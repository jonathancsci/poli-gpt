from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .routers import generate, search

app = FastAPI()
app.include_router(generate.router)
app.include_router(search.router)

app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")

@app.get("/")
def serve_root():
    return FileResponse('../frontend/index.html')

