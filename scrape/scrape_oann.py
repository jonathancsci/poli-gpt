import json
import requests
import os
from bs4 import BeautifulSoup
import http.client, urllib.parse
from dotenv import load_dotenv

load_dotenv()

news_api = os.getenv("THE_NEWS_API_KEY")

conn = http.client.HTTPSConnection('api.thenewsapi.com')

params = urllib.parse.urlencode({
    'api_token': news_api,
    'categories': 'politics',
    'published_on': '2024-01-10',
    'language': 'en',
    'locale': 'us',
    'domains': 'oann.com',
    'limit': 1
})

conn.request('GET', '/v1/news/all?{}'.format(params))

res = conn.getresponse()
data = res.read()

# Parse the JSON response
response_json = json.loads(data)
for article in response_json.get('data',[]):
    print(article['uuid'])
print(response_json.get('data'))
# Extract URLs from the data object
urls = [article['url'] for article in response_json.get('data', [])]
print(urls)

#Print the extracted URLs
for url in urls:


    # Fetch the content from the URL
    response = requests.get(url)
    html = response.content

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(html, 'html.parser')

    # Find the div that contains the article
    article_div = soup.find('div', class_='entry-content')

    # Extract all paragraph texts from the article div
    article_paragraphs = article_div.find_all('p')

    # Combine the texts of all paragraphs into a single string
    article_text = '\n\n'.join(paragraph.get_text(strip=True) for paragraph in article_paragraphs)

    file_path = 'oann_article.txt'

    with open(file_path, 'w') as file:
        file.write(article_text)




