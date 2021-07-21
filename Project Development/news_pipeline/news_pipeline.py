from sklearn.feature_extraction.text import CountVectorizer
import re
import requests
from datetime import date
from pymongo import MongoClient

#Open MongoDB connection
client = MongoClient()

#Create database/start connection to database
db = client.news
articles = db.news

class pull_updated_topic_list:
    def __init__(self):
        self.updated_topics = None

    def pull_topics(self):
        #Add code
        return print('finished')

class daily_news_api_pull_and_clean:

    def __init__(self, list_of_topics=None, database = db.articles):
        self.list_of_topics = list_of_topics
        self.database = database
        self.is_added_to_db = False

    def query_news_today(self, topic):
        query_date = str(date.today())
        url = "https://free-news.p.rapidapi.com/v1/search"
        querystring = {'q': topic,'lang':'en', 'from': query_date,'to': query_date, 'page_size':'100'}
        headers = {
            'x-rapidapi-key': '780fcaeeb3mshf9210d76d977dc2p1702dbjsn0f8d212f07b3',
            'x-rapidapi-host': 'free-news.p.rapidapi.com'
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        self.pull = response
        return response

    def query_topics(self):
        for topic in self.list_of_topics:
            try:
                working_query = self.query_news_today(topic)
                working_query = list(working_query['articles'])
                self.database.insert_many(working_query, ordered=False)
            except:
                continue
            self.is_added_to_db = True
        return print(self.database.count(), 'total articles in database')


class model_pipeline:

    def __init__(self, vectorizer=CountVectorizer(), tokenizer=None, cleaning_function=None, 
                 stemmer=None, lemm=None, model=None, database = db.articles):
        if not tokenizer:
            tokenizer = self.splitter
        if not cleaning_function:
            cleaning_function = self.clean_text
        self.stemmer = stemmer
        self.lemm = lemm
        self.tokenizer = tokenizer
        self.model = model
        self.database = database
        self.cleaning_function = cleaning_function
        self.vectorizer = vectorizer
        self._is_fit = False
        self.words = None
        self.topics = None
        self.article_list = None

    def query_article_db(self):
        article_list = []
        cursor = db.articles.find({}, {'_id':0, 'title': 1})
        for title in cursor:
            article_list.append(title['title'])
        self.article_list = article_list
    #Need to figure out how to remove duplicates
        return article_list
        
    def splitter(self, text):
        return text.split(' ')
        
    def clean_text(self, text, tokenizer, stemmer, lemm):
        cleaned_text = []
        for doc in text:
            cleaned_words = []
            for word in tokenizer(doc):
                low_word = re.sub('[\d\W]','', word).lower()
                if stemmer:
                    low_word = stemmer.stem(low_word)
                if lemm:
                    low_word = lemm.lemmatize(low_word)
                cleaned_words.append(low_word)
            cleaned_text.append(' '.join(cleaned_words))
        return cleaned_text 

#Need to update for word2vec - ask instructor
    def fit_transform(self, text):
        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer, self.lemm)
        self.words =  self.vectorizer.fit_transform(clean_text)
        self.topics = self.model.fit_transform(self.words)
        self._is_fit = True
        return self.topics

    def transform_new(self, text):
        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer, self.lemm)
        self.words_new =  self.vectorizer.transform(clean_text)
        self.topics_new = self.model.transform(self.words_new)
        return self.topics_new

    def print_topics(self, num_words=10):
        feat_names = self.vectorizer.get_feature_names()
        for topic_idx, topic in enumerate(self.model.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feat_names[i] for i in topic.argsort()[:-num_words - 1:-1]])
            print(message)