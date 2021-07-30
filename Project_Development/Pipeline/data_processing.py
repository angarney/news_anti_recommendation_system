#Bring in dependencies for functions
import requests
import pickle
import pandas as pd
from datetime import date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
import time

#Open MongoDB connection
client = MongoClient()

#Create database/start connection to database
db = client.news
articles = db.news

#Global variable
path = os.path.dirname(__file__)

#------------------------------------------------------------------------------

#Update topic list

def pull_topics():
    usnews_data_link = 'https://www.usnews.com/topics/subjects'
    #chrome_path = '/Applications/chromedriver'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(usnews_data_link)
    page_to_save = driver.page_source
    usnews_data_soup = BeautifulSoup(page_to_save, "lxml")
    driver.quit()
    list_of_topics = []
    for subject in usnews_data_soup.find_all('li', attrs={'class':'t link-dark'}):
        list_of_topics.append(subject.text)
    pickle.dump(list_of_topics, open('list_of_topics','wb'))

#------------------------------------------------------------------------------

#Pull articles for all topics

def query_topics(database, start_date):
    list_of_topics = pickle.load(open(path + '/Pickles/list_of_topics','rb'))

    #Query database for topic
    def query_news_today(topic, start_date):
        if start_date:
            query_start_date = start_date
        else:
            query_start_date = str(date.today())
        query_end_date = str(date.today())
        url = "https://free-news.p.rapidapi.com/v1/search"
        querystring = {'q': topic,'lang':'en', 'from': query_start_date,'to': query_end_date, 'page_size':'100'}
        headers = {
            'x-rapidapi-key': '780fcaeeb3mshf9210d76d977dc2p1702dbjsn0f8d212f07b3',
            'x-rapidapi-host': 'free-news.p.rapidapi.com'
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()

    for topic in list_of_topics:
        try:
            time.sleep(2)
            working_query = query_news_today(topic, start_date)
            working_query = list(working_query['articles'])
            database.insert_many(working_query, ordered=False)
        except:
            print(database.count(), 'as of ', topic)
            continue
    return print(database.count(), 'total articles added to database')

#------------------------------------------------------------------------------

#Query database and clean text

def query_update_clean(database):
    cursor = database.find({}, {'_id':0, 'title': 1, 'is_opinion': 1, 'author': 1, 'link': 1, 'published_date': 1, 'summary': 1, 'published_date': 1, 'topic': 1})
    article_headers = ['title', 'is_opinion', 'author', 'link', 'published_date', 'summary', 'published_date','topic']
    news_data = []

    for article in cursor:
        title = article['title']
        is_opinion = article['is_opinion']
        author = article['author']
        link = article['link']
        published_date = article['published_date']
        summary = article['summary']
        published_date = article['published_date']
        topic = article['topic']
        news_dict = dict(zip(article_headers, [title, is_opinion, author, link, published_date, summary, published_date, topic]))
        news_data.append(news_dict)

    #Convert to DataFrame
    news_df = pd.DataFrame(news_data)

    #Drop duplicates
    pre_drop_total = len(news_df)
    news_df.drop_duplicates(subset=['title'], inplace=True)
    post_drop_total = len(news_df)
    print(post_drop_total/pre_drop_total*100, '% of the total not dropped')

    #Convert to list for model processing
    full_news_docs = news_df['title'].to_list()

    #Pickle objects for easier future import
    pickle.dump(news_df, open(path + '/Pickles/news_df','wb'))
    pickle.dump(full_news_docs, open(path + '/Pickles/full_news_docs','wb'))

#------------------------------------------------------------------------------

def main():
    last_day_updated = pickle.load(open(path + '/Pickles/last_day_updated','rb'))
    pull_topics()
    query_topics(db.articles, start_date=last_day_updated)
    query_update_clean(db.articles)
    
    last_day_updated = date.today()
    pickle.dump(last_day_updated, open(path + '/Pickles/last_day_updated','wb'))


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()