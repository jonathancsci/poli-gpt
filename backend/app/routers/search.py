import os
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Database
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Query(BaseModel):
    text: str
    num_articles: int = 1

class Article(BaseModel):
    headline: str
    body: str
    url: str

class SearchResult(BaseModel):
    liberal: List[Article]
    conservative: List[Article]

class LiberalArticle(Base):
    __tablename__ = "liberal"
    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, index=True)
    body = Column(String)
    url = Column(String)

class ConservativeArticle(Base):
    __tablename__ = "conservative"
    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, index=True)
    body = Column(String)
    url = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Router
router = APIRouter(prefix='/search')

@router.post("/", response_model=SearchResult)
async def search_articles(query: Query, db=Depends(get_db)):
    liberal_articles = db.execute(text(f"""
        SELECT headline, body, url FROM liberal
        WHERE body LIKE :search_text
        OR headline LIKE :search_text
        LIMIT :limit
    """), {"search_text": f"%{query.text}%", "limit": query.num_articles}).fetchall()

    conservative_articles = db.execute(text(f"""
        SELECT headline, body, url FROM conservative
        WHERE body LIKE :search_text
        OR headline LIKE :search_text
        LIMIT :limit
    """), {"search_text": f"%{query.text}%", "limit": query.num_articles}).fetchall()

    if not liberal_articles and not conservative_articles:
        raise HTTPException(status_code=404, detail="Articles not found")

    return SearchResult(
        liberal=[Article(headline=article.headline, body=article.body, url=article.url) for article in liberal_articles],
        conservative=[Article(headline=article.headline, body=article.body, url=article.url) for article in conservative_articles]
    )

@router.get('/')
def serve_search():
    return {'text': 'not implemented yet'}

