#Bring in dependencies for functions
import pickle
import numpy as np
from nltk.tokenize import word_tokenize
import re
from pymongo import MongoClient
import os

#Global variable
path = os.path.dirname(__file__)

#Open MongoDB connection
client = MongoClient()

#Create database/start connection to database
db = client.news
articles = db.news

#------------------------------------------------------------------------------

#Function to clean/tokenize words

def clean_and_tokenize_all():
    news_df = pickle.load(open(path + '/Pickles/news_df','rb'))
    news_titles = news_df['title'].to_list()
    cleaned_title_words = []
    for document in news_titles:
        token_list = word_tokenize(document)
        cleaned_words = []
        for word in token_list:
            low_word = re.sub('[\d\W]', '', word).lower()
            if low_word:
                cleaned_words.append(low_word)
        cleaned_title_words.append(cleaned_words)
    return cleaned_title_words

#------------------------------------------------------------------------------

#Vectorize all docs and update news_df

def vectorize_all(cleaned_title_words):

    #Function to create document vectors
    def vectorize_document(cleaned_title_words, model):
        not_in_model = []
        list_of_word_vectors = []
        for token in cleaned_title_words:
            if token in model.wv.vocab:
                list_of_word_vectors.append(model[token])
            else:
                not_in_model.append(token)
        doc_vector = np.mean(list_of_word_vectors, axis=0)
        return doc_vector

    news_df = pickle.load(open(path + '/Pickles/news_df','rb'))

    word2vec_model = pickle.load(open(path + '/Pickles/word2vec_model','rb'))

    doc_vectors = []
    docs_not_added = []

    for i, document in enumerate(cleaned_title_words):
        for j, word in enumerate(document):
            doc_len = len(document)
            if word in word2vec_model.wv.vocab:
                doc_vectors.append(vectorize_document(document,word2vec_model))
                break
            elif j < doc_len - 1:
                continue
            else:
                docs_not_added.append(i)
    doc_vectors = np.vstack(doc_vectors)

    #Dump updated news_df
    news_df.drop(news_df.index[docs_not_added], inplace=True)
    pickle.dump(news_df, open(path + '/Pickles/news_df','wb'))

    #Pickle numpy array with word2vec article doc_vectors
    pickle.dump(doc_vectors, open(path + '/Pickles/doc_vectors','wb')) 

#------------------------------------------------------------------------------

def main():
    cleaned_title_words = clean_and_tokenize_all()
    vectorize_all(cleaned_title_words)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()