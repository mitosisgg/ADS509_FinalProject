import json
import os
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# altered to use /v2/everything so we can use from/to range
API_URL = "https://newsapi.org/v2/everything"  # changed API endpoint
PAGE_SIZE = 100
CATEGORIES = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

# Set the date range (YYYY-MM-DD). You can also set these in your .env
FROM_DATE = os.getenv("NEWS_START_DATE")
TO_DATE   = os.getenv("NEWS_END_DATE")

def fetch_articles(api_url, params=None):
    """
    Fetch articles from the NewsAPI endpoint.
    """
    try:
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        articles = payload.get('articles', [])
        return articles
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def main():
    """
    Fetch articles for each of the 7 categories and save them to JSON files.
    Keeps your loop shape, but now:
      - uses /v2/everything
      - sends 'q' (query) instead of 'category'
      - adds 'from' and 'to'
      - uses real pagination via 'page'
    """
    for category in CATEGORIES:
        # CHANGED: everything doesn't support country/category; use q + from/to
        base_params = {
            "q": category,
            "from": FROM_DATE,
            "to": TO_DATE,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": PAGE_SIZE,
            "apiKey": os.getenv("NEWS_API_KEY")
        }

        articles_list = []
        for i in range(10):  # still fetch up to 1000 articles per category
            params = dict(base_params)
            params["page"] = i + 1       # <<< changed (use proper pagination)
            print(f"Fetching page {params['page']} of {PAGE_SIZE} articles for topic '{category}' "
                  f"from {FROM_DATE} to {TO_DATE}")
            articles = fetch_articles(API_URL, params)
            if not articles:
                # stop early if we’re out of results
                break
            articles_list.extend(articles)

        # Keep original file naming
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_file = f"data/raw/{category}_articles_{current_date}.json"  # <<< changed

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(articles_list, f, indent=4)
        print(f"Saved {len(articles_list)} articles to {output_file}")


if __name__ == "__main__":
    if not os.getenv("NEWS_API_KEY"):
        raise SystemExit("ERROR: Set NEWS_API_KEY in your environment or .env file.")
    main()