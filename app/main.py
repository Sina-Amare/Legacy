# app/main.py
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

@app.get("/")
def read_root():
    """
    Root endpoint providing project info.
    """
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }