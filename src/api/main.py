from os import path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from .router import v1_router

STATIC_DIRECTORY_PATH = path.join(path.dirname(path.dirname(path.abspath(__file__))), "static")

app = FastAPI()
app.include_router(v1_router)
app.mount("/", StaticFiles(directory=STATIC_DIRECTORY_PATH, html=True), name="static")
