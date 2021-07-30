from Pipeline.data_processing import main as data_processing
from Pipeline.vader_sentiment import main as vader_sentiment
from Pipeline.word2vec_modeling import main as word2vec_modeling

#------------------------------------------------------------------------------

def main():
    data_processing()
    vader_sentiment()
    word2vec_modeling()
    
#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()