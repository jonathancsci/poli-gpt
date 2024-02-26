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


# In[ ]:


# Load environment variables
load_dotenv()


# In[3]:


# Function to generate dates for the last month
def generate_last_month_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]


# In[4]:


def save_to_gcp_bucket(bucket_name, file_name, data):
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise Exception('GOOGLE_APPLICATION_CREDENTIALS not set in the environment variables')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data, ensure_ascii=False))
    print(f"Data saved to {file_name} in bucket {bucket_name}")


# In[5]:


# Initialize EventRegistry
YOUR_API_KEY = "your_api_key_here"  
er = EventRegistry(apiKey = YOUR_API_KEY)


# In[6]:


# GCP Bucket Name
BUCKET_NAME = "fox_newsapi_ai_data"


# In[7]:


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
        "isDuplicate": "skipDuplicates"
      }
    }

    q = QueryArticlesIter.initWithComplexQuery(query)
    for article in q.execQuery(er, maxItems=100):
        file_name = f"foxnews_{formatted_date}_{article['uuid']}.json"
        save_to_gcp_bucket(BUCKET_NAME, file_name, article)

