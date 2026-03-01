"""
carwash_backend/main.py
Principal module to run the carwash backend application.
"""

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from common.config.database import test_connection
# 1. IMPORT ALL MODELS to register them in SQLAlchemy's Base metadata
# This prevents the "failed to locate a name ('Vehicle')" error.
from features.role.models import Role
from features.user.models import User
from features.vehicle.models import Vehicle
from features.service.models import Service
from features.appointment.models import Appointment
from features.auth.models import UserToken

# 2. Import routers
from features.user.routes import router as user_router
from features.auth.routes import router as auth_router
from features.vehicle.routes import router as vehicle_router
from features.service.routes import router as service_router
from features.appointment.routes import router as appointment_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events."""
    logger.info("Verificando conexión a Base de Datos...")
    status = await test_connection()

    if status is True:
        logger.info("✅ Database connection successful.")
    else:
        logger.error("❌ Critical Error: Could not connect to the database.")

    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="CarWash System API",
    version="1.0.0",
    lifespan=lifespan
)

# Register Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(vehicle_router)
app.include_router(service_router)
app.include_router(appointment_router)