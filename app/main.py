# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS Middleware

from app.core.config import settings
from app.api.endpoints import dynasties

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# --- CORS Middleware Setup ---
# This allows our frontend (running on a different port) to communicate with our backend.
origins = [
    "http://localhost:5173",  # The address of our SvelteKit frontend
    "http://localhost:3000",  # A common port for React dev servers
    "http://localhost:8080",  # A common port for Vue dev servers
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# --- End of CORS Setup ---

app.include_router(dynasties.router, prefix="/api/v1/dynasties", tags=["Dynasties"])

@app.get("/")
def read_root():
    return {"project_name": settings.PROJECT_NAME}