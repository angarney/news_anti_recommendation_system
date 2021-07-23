#Import streamlit
from os import write
import streamlit as st

#Import model packages
from sklearn.metrics import pairwise_distances
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import  NMF
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import os

#Import created pipeline class
from nlp_pipeline import nlp_pipeline

st.write("""
# News Article Anti-Recommender System
As the information access becomes increasingly online,
'echo chambers' have emerged as a growing concern. Often folks tend to consume and 
interact primarily with similar information. This can lead to heavily one-sided 
understandings of social issues. The following tool was designed to 
help people find content outside of their typically recommended content.   


 **Submit an article title to see article titles within the same topic
 from different perspectives.**
""")

with st.form(key='my_form'):
	input_query = st.text_input(label='Input article title here: ')
	submit_button = st.form_submit_button(label='Find Articles')

#Load in pickled objects

path = os.path.dirname(__file__)
topic_file = path+'/topic_model'
sent_score_file = path+'/sent_score_df'

topic_model = pickle.load(open(topic_file,'rb'))
sent_score_df = pickle.load(open(sent_score_file,'rb'))

#Sentiment function
def compound_sorter(score):
    if score > 0:
        return 1
    elif score == 0:
        return 0
    elif score < 0:
        return -1

#Recommender function

def article_opposite(input_query):

    #Find sentiment
    analyzer = SentimentIntensityAnalyzer()
    new_sentiment = compound_sorter(analyzer.polarity_scores(input_query)['compound']) #-1 negative, +1 positive

    #Find topic
    new_topic = topic_model.transform_new(input_query)
    potential_article_return_list = pairwise_distances(new_topic,topic_model.topics,metric='cosine').argsort()
    articles_to_return = []
    already_added_1 = False
    already_added_2 = False
    if new_sentiment == 0:
        for article in potential_article_return_list[0]:
            article_sentiment = sent_score_df.iloc[article]['sentiment']
            if (article_sentiment == 1) and (already_added_1 == False):
                articles_to_return.append(article)
                already_added_1 = True
            elif (article_sentiment == -1) and (already_added_2 == False):
                articles_to_return.append(article)
                already_added_2 = True
            elif (already_added_1 == True) and (already_added_2 == True):
                return articles_to_return
    elif new_sentiment == 1:
        for article in potential_article_return_list[0]:
            article_sentiment = sent_score_df.iloc[article]['sentiment']
            if (article_sentiment == 0) and (already_added_1 == False):
                articles_to_return.append(article)
                already_added_1 = True
            elif (article_sentiment == -1) and (already_added_2 == False):
                articles_to_return.append(article)
                already_added_2 = True
            elif (already_added_1 == True) and (already_added_2 == True):
                return articles_to_return
    elif new_sentiment == -1:
        for article in potential_article_return_list[0]:
            article_sentiment = sent_score_df.iloc[article]['sentiment']
            if (article_sentiment == 0) and (already_added_1 == False):
                articles_to_return.append(article)
                already_added_1 = True
            elif (article_sentiment == 1) and (already_added_2 == False):
                articles_to_return.append(article)
                already_added_2 = True
            elif (already_added_1 == True) and (already_added_2 == True):
                return articles_to_return

#Run function
if input_query:
    recommended_articles = article_opposite([str(input_query)])
    article_1 = sent_score_df.iloc[recommended_articles[0]]['article']
    article_2 = sent_score_df.iloc[recommended_articles[1]]['article']
    
    st.write("""
    ## Check-out there articles!
    """)
    st.write('Article 1: {art1}'.format(art1 = article_1))
    st.write('Article 2: {art2}'.format(art2 = article_2))
    


