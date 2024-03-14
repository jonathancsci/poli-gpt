from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .data.init_db import init_db
from .routers import generate, search

init_db()

app = FastAPI()
app.include_router(generate.router)
app.include_router(search.router)


origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")

@app.get("/")
def serve_root():
    return FileResponse('../frontend/index.html')

