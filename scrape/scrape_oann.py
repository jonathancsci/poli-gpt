import json
import requests
import os
from bs4 import BeautifulSoup
import http.client, urllib.parse
from dotenv import load_dotenv
import time
import urllib.request
import urllib.error

# def uptime_bot(url):
#     while True:
#         try:
#             conn = urllib.request.urlopen(url)
#         except urllib.error.HTTPError as e:
#             # Email admin / log
#             print(f'HTTPError: {e.code} for {url}')
#         except urllib.error.URLError as e:
#             # Email admin / log
#             print(f'URLError: {e.code} for {url}')
#         else:
#             # Website is up
#             print(f'{url} is up')
#         time.sleep(60)

load_dotenv()

news_api = os.getenv("THE_NEWS_API_KEY")

conn = http.client.HTTPSConnection('api.thenewsapi.com')

date = '2023-08-15'
print(f"running for {date}")

params = urllib.parse.urlencode({
    'api_token': news_api,
    'categories': 'politics,general',
    'published_on': date,
    'language': 'en',
    'locale': 'us',
    'domains': 'oann.com',
    'limit': 3
})

conn.request('GET', '/v1/news/all?{}'.format(params))

res = conn.getresponse()
data = res.read()

# Parse the JSON response
response_json = json.loads(data)
# for article in response_json.get('data',[]):
#     print(article['uuid'])

# Extract URLs from the data object
# urls = [article['url'] for article in response_json.get('data', [])]
# print(urls)

# Loop through each article in the response
for article in response_json.get('data', []):

    # uptime_bot(article['url'])
    # Fetch the content from the URL
    response = requests.get(article['url'])
    if response.status_code == 200:
        html = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(html, 'html.parser')

        # Find the div that contains the article
        article_div = soup.find('div', class_='entry-content')

        # Extract all paragraph texts from the article div
        article_paragraphs = article_div.find_all('p')

        # Combine the texts of all paragraphs into a single string
        article_text = '\n\n'.join(paragraph.get_text(strip=True) for paragraph in article_paragraphs)

        # Rename the 'snippet' key to 'article'
        article['article'] = article.pop('snippet')

        # Replace the 'snippet' field in the JSON with the article content
        article['article'] = article_text

        article_uuid = article['uuid']

        time.sleep(10)

        # Write the modified JSON to a file
        file_path = f"oann_{article_uuid}.json"
        with open(file_path, 'w') as file:
            json.dump(article, file, indent=4)

        print(f"article: {article_uuid} has been added")

    else:
        print(response.status_code)

