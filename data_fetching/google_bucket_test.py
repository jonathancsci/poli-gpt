from dotenv import load_dotenv
import os
from google.cloud import storage
import requests
from bs4 import BeautifulSoup
import json

# Load environment variables from .env file
load_dotenv()

# Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise Exception('GOOGLE_APPLICATION_CREDENTIALS not set in the environment variables')


# URL of the page you want to scrape
url = 'https://www.cnn.com/2024/01/30/politics/biden-jordan-attack-response/index.html'

# Fetch the content from the URL
response = requests.get(url)
html = response.content

# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(html, 'html.parser')

# Find the div that contains the article
article_div = soup.find('div', class_='article__content')

# Extract all paragraph texts from the article div
article_paragraphs = article_div.find_all('p', class_='paragraph')

# Combine the texts of all paragraphs into a single string
article_text = '\n\n'.join(paragraph.get_text(strip=True) for paragraph in article_paragraphs)

#GCS STUFF
storage_client = storage.Client()
bucket_name = 'news-data-poligpt'
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob('scraped_data.json')
blob.upload_from_string(article_text, content_type='application/json')
print(f'Data uploaded to {bucket_name}/scraped_data.json')
