
"""
This file contains all the code for the enitire analyis

This file is dependent on utility.py file
"""


#making necessary imports
from collections import defaultdict

from pandas.core.arrays import boolean
from nltk.tokenize import word_tokenize,sent_tokenize
import nltk
import pandas as pd
from utility import count_syllables

#sentiment main calss
class sentiment_analysis:


    #function to read the stop words from the url
    def get_stop_words(self):
        df = pd.read_csv('Input_files/StopWords_GenericLong.txt')
        return df

    #function to tokenize and remove stop words    
    def pre_process(self, article):
        #tokenize and remove the stop words
        tokenized_words = word_tokenize(article)
        stop_words = self.get_stop_words()
        for word in tokenized_words:
            #remove non-alphabeitc words
            if word.isalpha() == False:
                tokenized_words.remove(word)
            #remove stop words
            if word in stop_words:
                tokenized_words.remove(word) 
        return tokenized_words


    #function to read the master dictionary from url
    def get_master_dic(self):
        df = pd.read_csv('Input_files/MasterDictionary_2020.csv')
        master_dic = df[['Word', 'Positive', 'Negative']]
        return master_dic
    
    #function to get positive and negtive score for article
    def get_pos_neg_score(self, cleaned_words):
        master_df = self.get_master_dic()
        positive_score = 0
        negitive_score = 0
        appeared = defaultdict()
        
        #loop the cleaned words
        for index, word in enumerate(cleaned_words):
            word = word.upper()

            #check if word exixts in the master df
            if word not in master_df.values:
                pass
            else:
                #if it does then get the sub_Df so you dont loop with duplicates twice
                if word not in appeared:
                    appeared[word] = True
                    #getting the df where values match
                    sub_df = master_df[master_df['Word'] == word]
                    #looping the sub df to get positive and negitive values
                    for i,row in sub_df.iterrows():
                        if row['Positive']>0:
                            positive_score= positive_score+1
                        if row['Negative']>0:
                            negitive_score = negitive_score+1
                else:
                    pass
  
        return positive_score, (negitive_score )

    #function to get total words
    def get_total_words(self,text):
        count = 0
        for words in word_tokenize(text):
            if words.isalpha():
                count = count+1
        return count

    #function to get total sentnces
    def get_num_of_sentences(self, text):
        return len(sent_tokenize(text))
    

    #function to get number of complex words
    def get_complex_words(self, text):
        count=0
        for word in text:
            num_of_syl = self.get_syllables(word)
            if num_of_syl>2:
                count=count+1
        return count

    #function to get syllabus per word
    def syllables_per_word(self,text):
        num_of_syl = 0
        for word in text:
            num_of_syl = num_of_syl + self.get_syllables(word) 
        return num_of_syl
    
    #helper function to get syllabus for particular word
    def get_syllables(self, word):
        num_of_syl = count_syllables(word)
        return num_of_syl
    
    #function to get num of pronouns
    def get_num_of_pronouns(self, text):
        count = 0
        tk_words = word_tokenize(text)
        tagged_tuple = nltk.pos_tag(tk_words)
        for tuples in tagged_tuple:
            if tuples[1] == 'PRP':
                count = count+1
        return count


    #function to get num of char
    def get_num_of_char(self, text):
        count = 0
        tk_words = word_tokenize(text)
        for word in tk_words:
            for chr in word:
                count= count+1
        return count


    #main driver code for analysis
    def complete_analysis(self, article):

        final_dict = defaultdict(int)
        cleaned_text = self.pre_process(article)
        pos,neg = self.get_pos_neg_score(cleaned_text)

        #section 1 : Text Analysis
        final_dict['postive_score'] = pos
        final_dict['negitive_score'] = neg
        final_dict['polarity_score'] = (pos - neg)/((pos + neg) + 0.000001)
        final_dict['subjectivity_score'] = (pos + neg)/((len(cleaned_text)+0.000001))
        #print("checkpoint 2")


        total_words = self.get_total_words(article)
        total_sent = self.get_num_of_sentences(article)
        complex_words = self.get_complex_words(cleaned_text)
        #print("checkpoint 3")
        

        #section 2 : Readability
        final_dict['Avg_sentence_len'] = (total_words) / (total_sent)
        final_dict['Complex_word_count'] = (complex_words)/(total_words)
        final_dict['fog_index'] = 0.4 *(final_dict['Avg_sentence_len'] + final_dict['Complex_word_count'])
        #print("checkpoint 4")

        #section 3:
        final_dict['Avg_words_per_sent'] = total_words/total_sent
        final_dict['complex_words'] = complex_words
        final_dict['word_count'] = total_words
        final_dict['syllable_count_per_word'] = self.syllables_per_word(cleaned_text)/total_words
        final_dict['Personal_pronouns'] = self.get_num_of_pronouns(article)
        final_dict['avg_word_len'] = self.get_num_of_char(article)/total_words
        print("final_checkpoint")

        return final_dict

#test run code commented out


"""
if __name__ == "__main__":
    #text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum"
    s = sentiment_analysis()

    #test for cleaned text and master dict
    #cleaned = s.pre_process(text)
    #print("cleaned = ", cleaned)
    #m = s.get_master_dic()
    #print(m)

    #test for pornouns
    #text3 = "Hello ABANDON ABDICATIONS ABEYANCE my name is honey.I'm good how are you. i hope you are doing fine. we will have sex someday. I'm attarcted towards you. so please let me know if this is evil"
    #num = s.get_num_of_pronouns(text3)
     
    #test for pos and neg 
    #text4 = ['ABANDON', 'ABDICATIONS', 'BETTER']
    #p,n = s.get_pos_neg_score(text4)
    #print("pos = ", p, "neg = ", n)
 
    #test for analysis 
    #dictionary = dict({1 : text3})
    #print("dictionary  = ", dictionary)
    #result = s.sentiment(dictionary)
    #print(result)
"""