"""""
carwash_backend/features/appointment/routes.py
_routes for appointment feature_
"""
from typing import List
from fastapi import APIRouter, Depends, Query
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

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin"]))
):
    """
    Business Intelligence Dashboard.
    Provides daily revenue and status summary. Admin Only.
    """
    from common.utils.date_utils import get_now_mx
    from features.appointment.dao_stats import AppointmentStatsDAO

    today = get_now_mx().date()
    stats_dao = AppointmentStatsDAO(db)
    return await stats_dao.get_daily_stats(today)
@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
async def update_status(
    appointment_id: int,
    new_status: str = Query(..., description="Status ('Pending', 'In Progress', 'Completed', 'Cancelled')"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Washer"]))
):
    """
    Update the status of a specific appointment.
    Washers will use this to mark a car as 'In Progress' or 'Completed'.
    """
    controller = AppointmentController(db)
    return await controller.update_appointment_status(appointment_id, new_status, current_user)