"""""
carwash_backend/common/config/config.py
Application Configuration Module.

This module handles the loading and validation of environment variables
using Pydantic. It provides a centralized Settings class for the application.
"""

import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

#determined the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 2. Create the absolute path to the .env file
ENV_FILE_PATH = BASE_DIR / ".env"

print(f"Buscando .env en: {ENV_FILE_PATH}") # debugging line to confirm the path being used

class Settings(BaseSettings):
    APP_NAME: str = "Carwash API"
    DEBUG_MODE: bool = False

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # --- Pydantic Configuration ---
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,  # <--- use the absolute path to the .env file
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
