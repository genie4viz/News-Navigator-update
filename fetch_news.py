from google_news import GoogleNews
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration using environment variable
mongo_uri = os.getenv('MONGO_URI', 'default_mongo_uri_if_none_provided')
client = MongoClient(mongo_uri)
db = client['news_database']

def get_titles(keyword):
    news = []
    gn = GoogleNews(lang='en', country='IN')
    search = gn.search(keyword)
    articles = search.get('entries', [])
    for i in articles:
        article = {'title': i.get('title'), 'link': i.get('link'), 'published': i.get('published')}
        news.append(article)
    return news

def get_news_data():
    categories = ['WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'SCIENCE', 'SPORTS']
    news_data = {}
    category_counts = {}
    for category in categories:
        data = get_titles(category)
        df = pd.DataFrame(data)
        news_data[category] = df.to_dict(orient='records')
        category_counts[category] = len(df)
    return news_data, category_counts

def insert_data_into_mongodb(news_data):
    for category, articles in news_data.items():
        collection = db[category]
        collection.delete_many({})
        if articles:  # Check if there are articles to avoid empty inserts
            collection.insert_many(articles)
    print("Data successfully inserted into MongoDB.")

def fetch_and_update_news():
    news_data, category_counts = get_news_data()
    print("News Data:")
    for category, articles in news_data.items():
        print(f"\nCategory: {category}")
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Published: {article['published']}")
            print("-" * 40)
        print("=" * 60)
    print("\nTotal Number of Articles in Each Category:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")
    insert_data_into_mongodb(news_data)

if __name__ == "__main__":
    fetch_and_update_news()
