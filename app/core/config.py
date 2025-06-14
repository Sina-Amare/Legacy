# app/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legacy: An Alternate History Simulator"
    PROJECT_VERSION: str = "0.0.1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    class Config:
        case_sensitive = True

settings = Settings()