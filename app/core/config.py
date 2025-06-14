# app/core/config.py

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# This line loads the environment variables from the .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings are managed by this class.
    It reads environment variables and provides them in a type-safe manner.
    """
    PROJECT_NAME: str = "Legacy: An Alternate History Simulator"
    PROJECT_VERSION: str = "0.0.1"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # This class can be expanded with more settings as the project grows
    # e.g., API keys, secret keys, etc.

    class Config:
        case_sensitive = True

# Create a single instance of the settings to be used throughout the application
settings = Settings()