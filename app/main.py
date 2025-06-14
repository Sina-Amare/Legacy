# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints import dynasties, games

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

origins = ["http://localhost:5173"] # Frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The routers from other files are included here
app.include_router(dynasties.router, prefix="/api/v1/dynasties", tags=["Dynasties"])
app.include_router(games.router, prefix="/api/v1/games", tags=["Games"])

# The root endpoint must use the main 'app' object's decorator
@app.get("/")
def read_root():
    """
    Root endpoint for the application.
    Provides basic project information.
    """
    return {"project_name": settings.PROJECT_NAME}