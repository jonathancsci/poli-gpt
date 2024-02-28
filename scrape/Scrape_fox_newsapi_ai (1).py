#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install eventregistry


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
    start_date = end_date - timedelta(days=1)
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]


# In[5]:


def save_to_gcp_bucket(bucket_name, file_name, data):
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise Exception('GOOGLE_APPLICATION_CREDENTIALS not set in the environment variables')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data, content_type='application/json'))
    print(f"Data saved to {file_name} in bucket {bucket_name}")


# In[6]:


# Initialize EventRegistry
YOUR_API_KEY = "c5126a6e-03af-40f6-822a-866a29b00eac"  
er = EventRegistry(apiKey = YOUR_API_KEY)


# In[7]:


# GCP Bucket Name
BUCKET_NAME = "fox_newsapi_ai_data"


# In[8]:


# Iterate over dates for the last month
for date in generate_last_month_dates():
    formatted_date = date.strftime('%Y-%m-%d')
    print(f"Fetching articles for {formatted_date}")

    query = {
      "$query": {
        "$and": [
          {
            "categoryUri": "dmoz/News/Politics"
          },
          {
            "sourceUri": "foxnews.com"
          },
          {
            "dateStart": formatted_date,
            "dateEnd": formatted_date,
            "lang": "eng"
          }
        ]
      },
      "$filter": {
        "isDuplicate": "skipDuplicates",
        "dataType": [
                "news",
                "pr",
                "blog"
            ]
      }
    }
    
    q = QueryArticlesIter.initWithComplexQuery(query)
    for article in q.execQuery(er, maxItems=100):
        print(article)
        file_name = f"foxnews_{formatted_date}_{article['uri']}.json"
        save_to_gcp_bucket(BUCKET_NAME, file_name, article)
        print(f'Data uploaded to {bucket_name}/fox_{uri}.json')
        save_to_gcp_bucket(BUCKET_NAME, file_name, article)

