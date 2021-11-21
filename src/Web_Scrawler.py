
"""

This file contains the code for web scrapping
it is not dependent on any other file

"""

#making necessary imports
import requests
from bs4 import BeautifulSoup
#create a cralwer class with url as initalizer

class Crawler:
    
    def get_html_doc(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
        response = requests.get(url,headers=headers )
        return response.text

    def flatten(self,t):
        return [item for sublist in t for item in sublist]
    
    def crawl(self, url):
        html_document = self.get_html_doc(url)
        soup = BeautifulSoup(html_document, 'html.parser')
        article_content = " "
        #extracting the article title and article tags
        title = soup.find("h1", class_="entry-title").text
        article_content = article_content + title
        article_tag = soup.find("div", class_ = "td-post-content")
        #extarcting the article contents through nested tags 
        for ptag in article_tag.find_all(['p', 'ol','ul']):
            #article_contents.append(ptag.text)
            article_content = article_content + ptag.text

        return article_content


#test runs umcommented

#if __name__ == "__main__":
    #crawler = Crawler()
    #parsed_article = crawler.crawl("https://insights.blackcoffer.com/how-robots-can-help-in-e-learning-platforms/")
    #print(parsed_article)
    #print(type(parsed_article))
    #parsed_str = ''.join(parsed_article)
    #print("length = ", len(parsed_article))
    #print("parsed_str = ", parsed_str)
        
        

#write the crawler function to crawl the article 