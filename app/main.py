from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import api_router

app = FastAPI()

app.mount("/media", StaticFiles(directory="uploads"), name="media")
app.include_router(api_router)
