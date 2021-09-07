# Reducing Echo Chambers Through an Anti-Recommendation System

As information consumption moves primarily online, information echo chambers become inceasingly common. Data from ~160,000+ news articles were explored to create a anti-recommendation system. The purpose of the anti-recommendation system is to recommend article from a different perspective to users. The anti-recommendation system is built in sentiment system and Google's news pre-trained Word2Vec model. Moving forward:
* News aggregators and social media website should consider varying their recommendations algorithms to reduce echo chambers
* Utilizing current news sources increases the interpretability of recommendations
* Additional context around the recommendation helps make the articles more user friendly
* Future opportunities may include increasing the model processing speed and add CRON jobs to automate the fully connected pipeline

The following resources can be found in this repository:
* [Engineering Pipeline](https://github.com/angarney/Data_Engineering_Project/tree/main/Project_Development/Pipeline)
* [Topic Modeling Workflow](https://github.com/angarney/Data_Engineering_Project/blob/main/Project_Development/Modeling/topic_modeling_workflow.ipynb)
* [Streamlit App](https://github.com/angarney/Data_Engineering_Project/blob/main/Project_Development/streamlit_app.py)

**Check-out the presentation for this project [here](https://www.youtube.com/watch?v=H1N8YuW9ruA&feature=youtu.be)!**

## Design
News article titles were explored to create a recommendation system that would return articles from different perspectives. 
* **Opportunity:** Often folks tend to consume and interact primarily similar information. This can lead to heavily one-sided understandings social issues. 
* **Impact:** Increased access to articles from different perspectives
* **Data Science Solution Path:** Design an anti-recommendation system where someone can input an article title they are reading and be provided another article on the same topic from a different perspective
* **Impact Hypothesis:** Reading news content from a variety of perspectives will create a more informed public. 
* **Measures of Success:** Increased understanding for differences, increased reading of different perspectives


## Data

~160,000+ news articles from 2021 were obtained through the NewsCatcher API.  

**Features:** title, author, date published, summary, opinion (True/False), link, topic

[Data Link](https://newscatcherapi.com/)

## Algorithms
**Text Preprocessing:** Basic cleaning and tokenization were used 

**Neural Network:** Transfer learning was leveraged through Google's pre-trained Word2Vec model

**Sentiment Analysis:** All article were scores for sentiment

**Recommendation System:** A recommendation system was built using both the sentiment score and topic modeling

## Tools
* [Pandas](https://pandas.pydata.org/)/[NumPy](https://numpy.org/): Data cleaning/merging and exploratory data analysis
* [MongoDB](https://www.mongodb.com/): Database
* [PyMongo](https://pymongo.readthedocs.io/en/stable/): Database querying
* [Streamlit and Streamlit Sharing](https://streamlit.io/): App creating and hosting
* [vaderSentiment](https://pypi.org/project/vaderSentiment/): Sentiment analysis
* [Gensim](https://radimrehurek.com/gensim/): Model creation

## Communication
A [presentation](https://github.com/angarney/Data_Engineering_Project/blob/main/Presentation/news_072721.pdf) and app were created. 
