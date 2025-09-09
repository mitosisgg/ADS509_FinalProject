
import json
import os
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://newsapi.org/v2/top-headlines"
PAGE_SIZE = 100
CATEGORIES = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

def fetch_articles(api_url, params=None):
    """
    Fetch articles from the NEWS API top-headlines endpoint.

    Args:
        api_url (str): The API endpoint URL.
        params (dict, optional): Query parameters for the API request.

    Returns:
        list: A list of articles fetched from the API.
    """
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        payload = response.json()
        articles = payload.get('articles', [])
        return articles
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def main():
    """
    Fetch articles for each of the 7 categories and save them to JSON files.
    Each file is named with the category and the current date.
    Each request is limited to 100 articles, and we make 10 requests per category to fetch up to 1000 articles.
    """
    for category in CATEGORIES:
        params = {
            "country": "us",
            "pageSize": PAGE_SIZE,
            "category": category,
            "apiKey": os.getenv("NEWS_API_KEY")
        }
        articles_list = []
        for i in range(10):
            print(f"Fetching {PAGE_SIZE} articles for category '{category}'")
            articles = fetch_articles(API_URL, params)
            articles_list.extend(articles)
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_file = f"data/raw/{category}_articles_{current_date}.json"
        
        with open(output_file, 'w') as f:
            json.dump(articles_list, f, indent=4)
        print(f"Saved {len(articles_list)} articles to {output_file}")


if __name__ == "__main__":
    main()