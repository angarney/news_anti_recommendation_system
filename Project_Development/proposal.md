# Data Engineering Project Proposal

_This project will be building off the existing news anti recommendation system created for my unsupervised learning project._

**Question/Need: What is the framing question of your analysis, or the purpose of the model/system you plan to build? Who benefits from exploring this question or building this model/system?**  

As the information access becomes increasingly online, 'echo chambers' have emerged as a growing concern. 

Framing Question:
* Problem: Often folks tend to consume and interact primarily similar information. This can lead to heavily one-sided understandings social issues. 
* Data Science Solution Path: Design an anti-recommendation system where someone can input an article title they are reading and be provided another article on the same topic from a different perspective with the news article populated from a customized data pipeline. 
* Initial Impact Hypothesis: Reading news content from a variety of perspectives will create a more informed public. 
* Measures of success, both technical and non-technical: Increased understanding for differences, increased reading of different perspectives

**Data Description: What dataset(s) do you plan to use, and how will you obtain the data? What is an individual sample/unit of analysis in this project? What characteristics/features do you expect to work with? If modeling, what will you predict as your target?**

The individual unit will be one article. The dataset will be created using the NewsCatcherAPI. 

Features: article title, author, date published, summary, date published, topic, country, is opinion, url

[Data Link](https://free-docs.newscatcherapi.com/?python#introduction)

**Tools: How do you intend to meet the tools requirement of the project? Are you planning in advance to need or use additional tools beyond those required?**  

* Python text processing libraries
* Word2Vec
* MongoDB for storage
* CRON for automated data pulls
* Flask: to share the final tool

**MVP Goal: What would a minimum viable product (MVP) look like for this project?**  
The MVP will be the working data pipeline for a portion of the dataset. 