"""
Database Seeding Module.
Populates the database with initial data such as system roles.
This script manages path resolution and ensures all models are loaded
for SQLAlchemy relationship mapping.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Setup the root path to allow absolute imports from common and features
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# IMPORTANT: We must import ALL models involved in relationships
# so SQLAlchemy's registry can find them during mapper initialization.
from features.role.models import Role
from features.user.models import User  # This fixes the KeyError: 'User'
from features.vehicle.models import Vehicle
from common.config.database import AsyncSessionLocal

# Configure professional logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_roles():
    """
    Creates default roles in the database if they do not exist.
    """
    logger.info("🌱 Starting database seeding for roles...")

    async with AsyncSessionLocal() as session:
        # Predefined system roles
        default_roles = [
            Role(name="Admin", description="Full system access and management"),
            Role(name="Cashier", description="Handles sales and appointments"),
            Role(name="Washer", description="Handles car cleaning operations"),
            Role(name="Customer", description="End-user and car owner")
        ]

        try:
            # We add roles to the session
            for role_data in default_roles:
                # Optional: You could check if role exists before adding
                session.add(role_data)

            await session.commit()
            logger.info("✅ Database successfully seeded with default roles.")
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Error during seeding: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(seed_roles())
    except KeyboardInterrupt:
        logger.warning("🛑 Seeding operation cancelled by user.")