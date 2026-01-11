"""
Application Configuration
-------------------------
Centralized configuration management using Pydantic Settings. 
Loads environment variables and defines global project constants.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Movie Analytics Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    RAW_DATA_PATH: Path = BASE_DIR / "data" / "raw_movies.csv"
    CLEANED_DATA_PATH: Path = BASE_DIR / "data" / "cleaned_movies.csv"
    
    CORS_ORIGINS: list[str] = ["*"]
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
