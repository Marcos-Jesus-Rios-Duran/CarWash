"""""
carwash_backend/features/appointment/routes.py
_routes for appointment feature_
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.config.database import get_db
from common.security.permissions import RoleChecker
from features.user.models import User
from features.appointment.schemas import AppointmentCreate, AppointmentResponse
from features.appointment.controller import AppointmentController

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Customer"]))
):
    """Schedules a new car wash service."""
    controller = AppointmentController(db)
    return await controller.schedule_appointment(appointment, current_user)

@router.get("/", response_model=List[AppointmentResponse])
async def list_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Washer", "Customer"]))
):
    """Retrieves appointments filtered by user role permissions."""
    controller = AppointmentController(db)
    return await controller.get_visible_appointments(current_user)