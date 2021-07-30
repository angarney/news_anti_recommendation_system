#Bring in dependencies for functions
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pickle
import pandas as pd
import os

#Global variable
path = os.path.dirname(__file__)

#------------------------------------------------------------------------------

#Create dataframe with article sentiments

def create_sentiments():
    news_df = pickle.load(open(path + '/Pickles/news_df','rb'))
    news_titles = news_df['title'].to_list()
    sent_score_dict = {}
    analyzer = SentimentIntensityAnalyzer()
    for title in news_titles:
        vs = analyzer.polarity_scores(title)
        sent_score_dict[title] = vs['compound']

    sent_score_df = pd.DataFrame.from_dict(sent_score_dict, orient='index').reset_index()
    sent_score_df.columns = ['article','vader_compound']

    #Add general categories
    def compound_sorter(score):
        if score > 0:
            return 1
        elif score == 0:
            return 0
        elif score < 0:
            return -1

    sent_score_df['sentiment'] = sent_score_df['vader_compound'].apply(compound_sorter)

    pickle.dump(sent_score_df, open(path + '/Pickles/sent_score_df','wb')) 


#------------------------------------------------------------------------------

def main():
    create_sentiments()

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
