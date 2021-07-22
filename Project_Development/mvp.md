# Data Engineering MVP

I have created a news pipeline to pull APIs, clean data, and update my model. Below is a sample of my pipeline to pull daily APIs. Additionally, I have created an initial database through API pulls of ~70,000 current news articles. 

```
class daily_news_api_pull_and_clean:

    def __init__(self, list_of_topics=None, database = db.articles):
        self.list_of_topics = list_of_topics
        self.database = database
        self.is_added_to_db = False

    def query_news_today(self, topic):
        query_date = str(date.today())
        url = "https://free-news.p.rapidapi.com/v1/search"
        querystring = {'q': topic,'lang':'en', 'from': query_date,'to': query_date, 'page_size':'100'}
        headers = {
            'x-rapidapi-key': '780fcaeeb3mshf9210d76d977dc2p1702dbjsn0f8d212f07b3',
            'x-rapidapi-host': 'free-news.p.rapidapi.com'
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        self.pull = response
        return response

    def query_topics(self):
        for topic in self.list_of_topics:
            try:
                working_query = self.query_news_today(topic)
                working_query = list(working_query['articles'])
                self.database.insert_many(working_query, ordered=False)
            except:
                continue
            self.is_added_to_db = True
        return print(self.database.count(), 'total articles in database')
```
