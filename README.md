# ADS509_FinalProject

## Getting Started
1. Clone this repo to your local machine
2. Create a virtual environment in the root of the repo
3. Activate the venv: source .venv/bin/activate
4. pip install -r requirements.txt
5. Create an account with [NewsAPI](https://newsapi.org/account)
6. Generate a new API key
7. Save the API key into a .env file in the root of the repo (NEWS_API_KEY=<your_api_key>)
8. Run fetch_articles.py

## Task 1: Fetching articles from News API (Christian)
fetch_articles.py saves raw articles as JSON files in data/raw. 
Each of the 7 categories articles is saved into its own file


## Task 2: Schedule data extraction (Graham)
You will want to create a script to run fetch_articles.py once a day to accumulate more articles

## Task 3: Transform payload (Anna)
You will need to extract the relevant fields (category, title, description, content) and transform the json files in data/raw into a single 'articles.csv' file. Save the file to the data/ directory.

