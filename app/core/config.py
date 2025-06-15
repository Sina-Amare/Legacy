from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    """
    Manages all application settings using pydantic-settings.

    This class automatically loads variables from a `.env` file and the system
    environment, providing a single, type-safe source of truth for configuration.
    """
    # model_config is the modern way (Pydantic V2) to configure settings behavior.
    # It replaces the older 'class Config' and the manual `load_dotenv()` call.
    model_config = SettingsConfigDict(
        env_file=".env",              # Specifies the .env file to load
        env_file_encoding="utf-8",    # Specifies the encoding of the .env file
        case_sensitive=True,          # Enforces case-sensitivity for env vars
        extra='ignore'                # Ignores extra variables in the .env file
    )

    PROJECT_NAME: str = "Legacy: An Alternate History Simulator"
    PROJECT_VERSION: str = "0.0.1"

    # --- Database Settings ---
    # This will be read directly from the DATABASE_URL in the .env file.
    DATABASE_URL: str

    # --- Celery Settings ---
    # These will be read from .env, or use these defaults if not found.
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # --- AI Settings for OpenRouter ---
    # These will be read from .env. SecretStr provides security for the API key.
    OPENROUTER_API_KEY: SecretStr
    OPENROUTER_API_BASE: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL_NAME: str = "deepseek/deepseek-chat-v3-0324:free"


# A single, global instance of the settings. On instantiation, it automatically
# performs the loading and validation based on the model_config.
# NOTE: Static analysis tools like Pylance may show a warning here about
# "missing arguments". This is expected, as the linter cannot predict the
# variables that will be loaded from the .env file at runtime. The code is
# correct and will execute without issues.
settings = Settings()