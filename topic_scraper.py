#Import necessary packages
from selenium import webdriver
from bs4 import BeautifulSoup
import pickle

#Pull in US News and World Report Subjects - update weekly
usnews_data_link = 'https://www.usnews.com/topics/subjects'

#Use selenium for webscraping
chrome_path = r'/Applications/chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get(usnews_data_link)
page_to_save = driver.page_source
usnews_data_soup = BeautifulSoup(page_to_save, "lxml")
driver.quit()

#Pull topics 
list_of_topics = []
for subject in usnews_data_soup.find_all('li', attrs={'class':'t link-dark'}):
    list_of_topics.append(subject.text)

#Pickle final list
pickle.dump(list_of_topics, open('list_of_topics','wb'))