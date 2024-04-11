#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install eventregistry


# In[2]:


import os
from eventregistry import *
from datetime import datetime, timedelta
from google.cloud import storage
from dotenv import load_dotenv
import json

# In[3]:


# Load environment variables
load_dotenv()


# In[4]:


# Function to generate dates for the last month
def generate_last_month_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]


# In[5]:


def save_to_gcp_bucket(bucket_name, file_name, data):
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise Exception('GOOGLE_APPLICATION_CREDENTIALS not set in the environment variables')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data))
    print(f"Data saved to {file_name} in bucket {bucket_name}")


# In[6]:


# Initialize EventRegistry
YOUR_API_KEY = os.getenv("NEWSAPI_AI_KEY")
er = EventRegistry(apiKey=YOUR_API_KEY)

# In[7]:


# GCP Bucket Name
BUCKET_NAME = "left_news_data"
# Sources to iterate over
sources = ["cnn.com", "msnbc.com"]

# In[10]:


# Iterate over dates for the last month
for date in generate_last_month_dates():
    formatted_date = date.strftime('%Y-%m-%d')
    for source in sources:
        print(f"Fetching articles from {source} for {formatted_date}")
        query = {
            "$query": {
                "$and": [
                    {"categoryUri": "news/Politics"},
                    {"sourceUri": er.getSourceUri(source)},  # Dynamically setting sourceUri
                    {"dateStart": formatted_date, "dateEnd": formatted_date, "lang": "eng"}
                ]
            },
            "$filter": {"dataType": ["news", "pr", "blog"]}
        }

        q = QueryArticlesIter.initWithComplexQuery(query)
        for article in q.execQuery(er, maxItems=100):
            print(article)
            file_name = f"{source}_{formatted_date}_{article['uri']}.json".replace('www.', '')
            save_to_gcp_bucket(BUCKET_NAME, file_name, article)
            print(f'Data uploaded to {BUCKET_NAME}/{file_name}')
