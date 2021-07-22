from sklearn.feature_extraction.text import CountVectorizer
import re
import pickle

class nlp_pipeline:

    def __init__(self, vectorizer=CountVectorizer(), tokenizer=None, cleaning_function=None, 
                 stemmer=None, lemm=None, model=None):
        if not tokenizer:
            tokenizer = self.splitter
        if not cleaning_function:
            cleaning_function = self.clean_text
        self.stemmer = stemmer
        self.lemm = lemm
        self.tokenizer = tokenizer
        self.model = model
        self.cleaning_function = cleaning_function
        self.vectorizer = vectorizer
        self._is_fit = False
        self.words = None
        self.topics = None
        
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