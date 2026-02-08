"""
carwash_backend/common/database/create_db.py
script to create tables if not exist
"""
import asyncio
import sys
from pathlib import Path

# Fix path to root
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from common.config.database import engine, Base

# Models Import
from features.role.models import Role
from features.user.models import User
from features.customer.models import Customer
from features.service.models import Service
from features.vehicle.models import Vehicle
from features.appointment.models import Appointment

async def create_tables():
    print("🚀 Init config db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ create table ")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())
