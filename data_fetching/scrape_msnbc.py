import os
from google.cloud import storage
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import json
import time
import random

# Define the range of random wait time in seconds
min_wait_time = 3  # Minimum wait time in seconds
max_wait_time = 10

# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment variables
api_key = os.getenv("THE_NEWS_API_KEY")

# Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise Exception('GOOGLE_APPLICATION_CREDENTIALS not set in the environment variables')
storage_client = storage.Client()
bucket_name = 'news-data-poligpt'
bucket = storage_client.bucket(bucket_name)

start_date = datetime.today()
num_days = 2  # For example, go back 10 days
dates_list = []
for i in range(num_days):
    # Calculate the date to iterate
    date_to_iterate = start_date - timedelta(days=i)
    # Append the date to the list
    dates_list.append(date_to_iterate.strftime("%Y-%m-%d"))


def fetch_news(api_key, date):
    url = f"https://api.thenewsapi.com/v1/news/all?api_token={api_key}&domains=msnbc.com&categories=politics&language=en&published_on={date}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            articles = data["data"]
            for article in articles:
                print(article['title'])
                print(article['url'])
                print("-" * 50)
            return articles
        else:
            print("Error occurred:", data['message'])

    except Exception as e:
        print("Error:", e)


def fetch_text(url):
    # Fetch the content from the URL
    response = requests.get(url)
    html = response.content

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(html, 'html.parser')

    # Find the div with class "showblog-body__content"
    content_div = soup.find("div", class_="showblog-body__content")

    # Extract text from all <p> elements inside the div
    if content_div:
        paragraphs = content_div.find_all("p")
        # Combine the texts of all paragraphs into a single string
        article_text = '\n\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)

        return article_text
    return False


def add_text(articles):
    for article in articles:
        wait_time = random.uniform(min_wait_time, max_wait_time)
        print(f"Waiting for {wait_time:.2f} seconds before next request...")
        time.sleep(wait_time)
        text = fetch_text(article["url"])
        if text:
            article["article"] = text


for day in dates_list:
    articles = fetch_news(api_key, day)
    add_text(articles)
    for article in articles:
        if "article" in article:
            uuid = article["uuid"]
            blob = bucket.blob(f"msnbc_{uuid}.json")
            json_data = json.dumps(article)
            blob.upload_from_string(json_data, content_type='application/json')
            print(f'Data uploaded to {bucket_name}/msnbc_{uuid}.json')
