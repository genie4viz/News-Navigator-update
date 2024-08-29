from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# MongoDB configuration using environment variable
mongo_uri = os.getenv('MONGO_URI', 'your_default_connection_string_if_any')
client = MongoClient(mongo_uri)
db = client['news_database']

def get_articles(category, page=1, per_page=5):
    """
    Fetch articles from MongoDB based on the category and pagination.
    """
    collection = db[category]
    skip = (page - 1) * per_page
    articles = collection.find().skip(skip).limit(per_page)
    return list(articles)

@app.route('/')
def home():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/fetch_news', methods=['GET'])
def get_all_articles():
    """
    Fetch articles from a specific category and return as JSON with pagination.
    """
    category = request.args.get('category', 'WORLD')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 5))
    
    articles = get_articles(category, page, per_page)
    data = [
        {
            "title": article.get("title", "No Title"),
            "link": article.get("link", "#"),
            "pubDate": article.get("published", "")
        } for article in articles
    ]
    
    return jsonify(data)
