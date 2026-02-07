"""""
carwash_backend/common/config/database.py
databse conection configuration for the application

This module handles the SQLAlchemy setup and provides a specific function
to test connectivity, adhering to the Single Responsibility Principle.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from .config import get_settings

# 1. Load configuration
settings = get_settings()

# 2. Create the Async Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG_MODE
)

# 3. Create the Session Factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Declarative Base
Base = declarative_base()


async def get_db():
    """
    Dependency function to get a database session for endpoints.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            pass


async def test_connection() -> bool | int:
    """
    Tests the database connectivity explicitly.

    Returns:
        True: If the connection is successful.
        -1: If the connection fails.
    """
    try:
        # We use a separate connection just to test 'SELECT 1'
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
            return True
    except Exception as e:
        # Log the specific error here if needed (e.g., print(e))
        return -1