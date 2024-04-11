#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random
import time
import requests


# In[14]:


# Load environment variables
#load_dotenv()


# In[3]:


def format_date(date):
    return date.strftime('%Y-%m-%d')

def generate_dates(start_date, end_date):
    return [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]


# In[15]:


def fetch_news(api_key, published_on, category='politics', country='us', language='en', limit=3):
    base_url = "https://api.thenewsapi.com/v1/news/all"
    params = {
        'api_token': api_key,
        'categories': category,
        'language': language,
        'country': country,
        'published_on': published_on,
        'domains': 'foxnews.com',  
        'limit': limit
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch news. Status Code: {response.status_code}")
        return {}


# In[12]:


def scrape_article(url):
    try:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        article_content = soup.find('article')  
        if not article_content:
            article_content = soup.find('div', attrs={'role': 'article'})  
        paragraphs = article_content.find_all(['p', 'h2', 'h3']) 
        article_text = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs if paragraph.get_text(strip=True))
        return article_text if article_text else "Article content not found." 
    except Exception as e:
        return f"Failed to scrape the article: {e}"


# In[6]:


def save_to_text_file(file_name, data):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(data)
        print(f"Data saved to {file_name} locally.")  
    except Exception as e:
        print(f"Failed to save data to {file_name}: {e}")  


# In[16]:


def main():
    API_KEY = ""
    if not API_KEY:
        print("API_KEY is not set. Please check your .env file.")
        return
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now()
    dates = generate_dates(start_date, end_date)

    for date in dates:
        formatted_date = format_date(date)
        print(f"Processing date: {formatted_date}")
        try:
            news_data = fetch_news(API_KEY, formatted_date)
            if 'data' not in news_data:
                print(f"No data found for {formatted_date}, or there was an error fetching the news.")
                continue
            articles = news_data.get('data', [])
        except Exception as e:
            print(f"Failed to fetch news for {formatted_date}: {e}")
            continue
        
        for i, article in enumerate(articles, start=1):
            try:
                print(f"Scraping article {i} of {len(articles)} for {formatted_date}")
                if 'url' not in article or not article['url']:
                    print("Article URL is missing. Skipping article.")
                    continue
                article_content = scrape_article(article['url'])
                article_data = {
                    "title": article.get('title', 'Unknown title'),
                    "url": article['url'],
                    "article": article_content,
                    #"news_outlet": article.get('source', {}).get('name', 'Unknown'),
                    #"published_on": article.get('published_at', 'Unknown date')
                }
                file_name = f"fox_news_{formatted_date}_{i}.txt"
                save_to_text_file(file_name, json.dumps(article_data,indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error processing article {i} for {formatted_date}: {e}")
            
            time.sleep(random.randint(3, 10))

if __name__ == "__main__":
    main()


# In[ ]:




