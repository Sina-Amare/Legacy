from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    """
    Manages all application settings using pydantic-settings.
    This class automatically loads variables from a .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'
    )

    PROJECT_NAME: str = "Legacy: An Alternate History Simulator"
    PROJECT_VERSION: str = "0.0.1"

    DATABASE_URL: str
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    OPENROUTER_API_KEY: SecretStr
    OPENROUTER_API_BASE: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL_NAME: str = "mistralai/mistral-7b-instruct"

settings = Settings()