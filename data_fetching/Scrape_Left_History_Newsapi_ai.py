#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from eventregistry import *
from datetime import datetime, timedelta
from google.cloud import storage
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


# In[ ]:


def generate_dates_from_start(start_date, days_diff):
    """
    Generate a list of dates starting from 'start_date' for 'days_diff' days.

    Args:
    - start_date (datetime): The start date from which to generate dates.
    - days_diff (int): The number of days to generate dates for.

    Returns:
    - List[datetime]: A list of datetime objects starting from 'start_date'.
    """
    return [start_date + timedelta(days=i) for i in range(days_diff + 1)]


# In[1]:


def save_to_gcp_bucket(bucket_name, file_name, data):
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise Exception('GOOGLE_APPLICATION_CREDENTIALS not set in the environment variables')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data))
    print(f"Data saved to {file_name} in bucket {bucket_name}")


# In[ ]:


# Initialize EventRegistry
YOUR_API_KEY = os.getenv("REAL_NEWSAPI_AI_KEY")
er = EventRegistry(apiKey=YOUR_API_KEY)

# GCP Bucket Name
BUCKET_NAME = "left_news_data"

# Sources to iterate over
#sources = "cnn.com", "msnbc.com", nytimes

# History start date
start_date = datetime(2023, 11, 7)
days_diff = 91

# In[ ]:


# Iterate over generated dates
for date in generate_dates_from_start(start_date, days_diff):
    formatted_date = date.strftime('%Y-%m-%d')
    print(f"Fetching articles for {formatted_date}")
    query = {
        "$query": {
            "$and": [
                {
                    "categoryUri": "news/Politics"
                },
                {
                    "$or": [
                        {
                            "sourceUri": "cnn.com"
                        },
                        {
                            "sourceUri": "msnbc.com"
                        },
                        {
                            "sourceUri": "nytimes.com"
                        }
                    ]
                },
                {
                    "dateStart": formatted_date,
                    "dateEnd": formatted_date,
                    "lang": "eng"
                }
            ]
        },
        "$filter": {
            "dataType": ["news", "pr", "blog"]
        }
    }

    q = QueryArticlesIter.initWithComplexQuery(query)
    for article in q.execQuery(er, maxItems=100):
        print(article)
        source = article['source']['uri']
        file_name = f"{source}_{formatted_date}_{article['uri']}.json".replace('www.', '')
        save_to_gcp_bucket(BUCKET_NAME, file_name, article)
        print(f'Data uploaded to {BUCKET_NAME}/{file_name}')
