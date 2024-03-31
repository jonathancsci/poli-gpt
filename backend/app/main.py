from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .data.init_db import init_db
from .routers import generate, search

init_db()

app = FastAPI()
app.include_router(generate.router)
app.include_router(search.router)

#app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

@app.get("/")
def serve_root():
    return FileResponse('../frontend/index.html')
