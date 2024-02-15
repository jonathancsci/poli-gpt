import os
from eventregistry import *
from dotenv import load_dotenv
load_dotenv()

EVENT_REGISTRY_API_KEY = os.getenv('EVENT_REGISTRY_API_KEY')
er = EventRegistry(apiKey=EVENT_REGISTRY_API_KEY)

usUri = er.getLocationUri("USA")

query = {
  "$query": {
    "$and": [
      {
        "categoryUri": "news/Politics"
      },
      {
        "sourceUri": "cnn.com"
      },
      {
        "lang": "eng"
      }
    ]
  },
  "$filter": {
    "forceMaxDataTimeWindow": "31"
  }
}
q = QueryArticlesIter.initWithComplexQuery(query)
# change maxItems to get the number of results that you want
for article in q.execQuery(er, maxItems=1):
    print(article)