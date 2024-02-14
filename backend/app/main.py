# Imports
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine

import torch

# Database
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")

if not (POSTGRES_PASSWORD and POSTGRES_USER and POSTGRES_DB):
    raise ValueError("Failed to load postgres environment variables")

# Testing database connection
connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"
engine = create_engine(connection_string)
try:
    connection = engine.connect()
except Exception as e:
    print(e)
finally:
    if connection:
        connection.close()

# App
app = FastAPI()

app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")

@app.get("/")
def serve_root():
    return FileResponse('../frontend/index.html')

@app.get("/api")
def test_api():
    return {"hello": "world!!!"}

@app.get('/test_torch')
def test_torch():
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'

    return {"device": device}
