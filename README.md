# Data_Engineering_Project

As information consumption moves primarily online, information echo chambers become inceasingly common. Data from ~204,000 news articles were explored to create a anti-recommendation system. The purpose of the anti-recommendation system is to recommend article from a different perspective to users. The anti-recommendation system is built in sentiment system and a topic modeling. Moving forward:
* News aggregators and social media website should consider varying their recommendations algorithms to reduce echo chambers
* Any anti-news recommendation systems should also include an algorithm around fact-based news
* Future opportunities may include adding collaborative filtering, updating the topic modeling, and creating a pipeline to include more update news articles in the dataset

The following resources can be found in this repository:
* [NLP Pipeline Class](https://github.com/angarney/Unsupervised_Project/tree/main/Project%20Development/nlp_pipeline)
* [Topic Modeling Workflow](https://github.com/angarney/Unsupervised_Project/blob/main/Project%20Development/topic_modeling_workflow.ipynb)
* [Recommender System Workflow](https://github.com/angarney/Unsupervised_Project/blob/main/Project%20Development/recommender_workflow.ipynb)
* [Streamlit App](https://github.com/angarney/Unsupervised_Project/blob/main/streamlit_app.py)

**Check-out the interactive app [here](https://share.streamlit.io/angarney/unsupervised_project/main)!**

## Design
News article titles were explored to create a recommendation system that would return articles from different perspectives. 
* **Opportunity:** Often folks tend to consume and interact primarily similar information. This can lead to heavily one-sided understandings social issues. 
* **Impact:** Increased access to articles from different perspectives
* **Data Science Solution Path:** Design an anti-recommendation system where someone can input an article title they are reading and be provided another article on the same topic from a different perspective
* **Impact Hypothesis:** Reading news content from a variety of perspectives will create a more informed public. 
* **Measures of Success:** Increased understanding for differences, increased reading of different perspectives


## Data

~204,000 news articles from 2008-2018 were obtained. 

**Features:** article title, author, date published, content, year of publishing, month of publishing, publication source, digital (yes/no), section, url

[Data Link](https://components.one/datasets/all-the-news-articles-dataset)

## Algorithms
**Text Preprocessing:** Lemmatization, tokenization, stopword removal were all used to clean the text data. 

**Unsupervised Model Building/Dimensionality Reduction:** Several models were tried and the final model selected was a Non-Negative Matrix Factorization for topic modeling

**Sentiment Analysis:** All article were scores for sentiment

**Recommendation System:** A recommendation system was built using both the sentiment score and topic modeling

## Tools
* [Pandas](https://pandas.pydata.org/)/[NumPy](https://numpy.org/): Data cleaning/merging and exploratory data analysis
* [Scikit-Learn](https://scikit-learn.org/stable/): Topic Modeling
* [Natural Language Toolkit](https://www.nltk.org/): Topic Modeling
* [DB Browser](https://sqlitebrowser.org/): Database
* [SQAlchemy](https://www.sqlalchemy.org/): Database querying
* [Streamlit and Streamlit Sharing](https://streamlit.io/): App creating and hosting
* [vaderSentiment](https://pypi.org/project/vaderSentiment/): Sentiment analysis
* Python Class Creation: NLP Pipeline class created

## Communication
A [presentation](https://github.com/angarney/Unsupervised_Project/blob/main/Presentation/news_062521.pdf) and [app](https://share.streamlit.io/angarney/unsupervised_project/main) were created. 