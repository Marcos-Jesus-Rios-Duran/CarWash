"""""
carwash_backend/common/config/config.py
Configuration file for the application
"""
from pydantic import BaseSettings
"validate that the environment variables for the database exist and are of the correct type"
class Settings(BaseSettings):
    # Database configuration
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Server configuration
    SERVER_HOST: str
    SERVER_PORT: int

    # Security
    SECRET_KEY: str