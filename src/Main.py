
"""
This file contains the driver code 

This is the mail file and is dependent on Web_Scrwaler.py and Sentiment.py and 
utility.py

"""

#making all the necessary imports
from collections import defaultdict
import pandas as pd
import pickle
from Sentiment import sentiment_analysis
from Web_Scrawler import Crawler
from utility import writer

#reading the input file into dataframe object
df = pd.read_csv('Input_files/Input2.csv')

articles = df['URL']
article_id = df['URL_ID']


crawler = Crawler()
article_dict = defaultdict(dict)
row_list = []

#loop through each article url
for index,url in enumerate(articles):
    #crawl the article
    print("index = ", index)
    parsed_article = crawler.crawl(url)
    #do the analysis of the crawled article
    s = sentiment_analysis()
    #stroe the complete anaylsis result 
    result_dict = s.complete_analysis(parsed_article)
    result_dict['Url'] = url
    row_list.append(result_dict)

#write to an output xlsx file
writer(row_list, 'Output_files/output.xlsx')

