from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints import dynasties, games, decisions

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# CORS Middleware setup to allow requests from the frontend
origins = [
    "http://localhost:5173", # Default SvelteKit dev server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the API routers
app.include_router(dynasties.router, prefix="/api/v1/dynasties", tags=["Dynasties"])
app.include_router(games.router, prefix="/api/v1/games", tags=["Games"])
app.include_router(decisions.router, prefix="/api/v1/decisions", tags=["Decisions"])

@app.get("/")
def read_root():
    """
    Root endpoint for the application.
    Provides basic project information.
    """
    return {"project_name": settings.PROJECT_NAME}