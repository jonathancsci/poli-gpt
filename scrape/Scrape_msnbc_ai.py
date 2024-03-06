import os

from eventregistry import *
from google.cloud import storage
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment variables
api_key = os.getenv("NEWSAPI_AI_KEY")

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

for day in dates_list:
    er = EventRegistry(apiKey=api_key)
    query = {
        "$query": {
            "$and": [
                {
                    "categoryUri": "news/Politics"
                },
                {
                    "sourceUri": "msnbc.com"
                },
                {
                    "dateStart": day,
                    "dateEnd": day,
                    "lang": "eng"
                }
            ]
        },
        "$filter": {
            "dataType": [
                "news",
                "pr",
                "blog"
            ]
        }
    }
    q = QueryArticlesIter.initWithComplexQuery(query)
    # change maxItems to get the number of results that you want
    for article in q.execQuery(er, maxItems=100):
        print(article)
        uri = article["uri"]
        blob = bucket.blob(f"msnbc_{uri}.json")
        json_data = json.dumps(article)
        blob.upload_from_string(json_data, content_type='application/json')
        print(f'Data uploaded to {bucket_name}/msnbc_{day}_{uri}.json')
