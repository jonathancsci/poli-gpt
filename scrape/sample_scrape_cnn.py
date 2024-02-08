import requests
from bs4 import BeautifulSoup

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

file_path = 'cnn_article.txt'

with open(file_path, 'w') as file:
    file.write(article_text)

