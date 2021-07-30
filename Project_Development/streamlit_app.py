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
from nltk.tokenize import word_tokenize
import re
import numpy as np

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

sent_score_df = pickle.load(open(path + '/Pipeline/Pickles/sent_score_df','rb'))
news_df = pickle.load(open(path + '/Pipeline/Pickles/news_df','rb'))
word2vec_model = pickle.load(open(path + '/Pipeline/Pickles/word2vec_model','rb'))
doc_vectors = pickle.load(open(path + '/Pipeline/Pickles/doc_vectors','rb'))

#Sentiment function
def compound_sorter(score):
    if score > 0:
        return 1
    elif score == 0:
        return 0
    elif score < 0:
        return -1

#Function to clean/tokenize words
def clean_and_tokenize(document):
    token_list = word_tokenize(document)
    cleaned_words = []
    for word in token_list:
        low_word = re.sub('[\d\W]', '', word).lower()
        if low_word:
            cleaned_words.append(low_word)
    return cleaned_words

#Function to create document vectors
def vectorize_document(cleaned_title_words, model):
    list_of_word_vectors = []
    for token in cleaned_title_words:
        if token in model.wv.vocab:
            list_of_word_vectors.append(model[token])
        else:
            continue
    doc_vector = np.mean(list_of_word_vectors, axis=0)
    return doc_vector

#Recommender function

def article_opposite(input_query, model, doc_vectors):

    #Find sentiment
    analyzer = SentimentIntensityAnalyzer()
    new_sentiment = compound_sorter(analyzer.polarity_scores(input_query)['compound']) #-1 negative, +1 positive

    #Find topic
    new_topic = vectorize_document(clean_and_tokenize(input_query), model).reshape(1, -1)
    potential_article_return_list = pairwise_distances(new_topic,doc_vectors,metric='cosine').argsort()
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
    recommended_articles = article_opposite(str(input_query),word2vec_model,doc_vectors)
    article_1 = news_df.iloc[recommended_articles[0]]['title']
    article_2 = news_df.iloc[recommended_articles[1]]['title']
    link_1 = news_df.iloc[recommended_articles[0]]['link']
    link_2 = news_df.iloc[recommended_articles[1]]['link']
    author_1 = news_df.iloc[recommended_articles[0]]['author']
    author_2 = news_df.iloc[recommended_articles[1]]['author']
    opinion_1 = news_df.iloc[recommended_articles[0]]['is_opinion']
    opinion_2 = news_df.iloc[recommended_articles[1]]['is_opinion']
    summary_1 = news_df.iloc[recommended_articles[0]]['summary']
    summary_2 = news_df.iloc[recommended_articles[1]]['summary']

    st.write("""
    ## **Check-out there articles!**
    """)

    st.write("""
    ## Article 1
    """)
    st.write('{art1} by {aut1}'.format(art1 = '['+str(article_1)+']('+str(link_1)+')', aut1=author_1))
    if opinion_1 is True:
        st.write('Please note, this recommended article is an opinion piece.')
    st.write('Article Summary: {sum1}'.format(sum1=summary_1))

    st.write("""
    ## Article 2
    """)
    st.write('{art2} by {aut2}'.format(art2 = '['+str(article_2)+']('+str(link_2)+')', aut2=author_2))
    if opinion_2 is True:
        st.write('Please note, this recommended article is an opinion piece.')
    st.write('Article Summary: {sum2}'.format(sum2=summary_2))

    


