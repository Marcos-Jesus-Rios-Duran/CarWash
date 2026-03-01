"""
Appointment Controller Module.
Orchestrates appointment rules, pricing, and role-based filtering.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.utils.date_utils import get_now_mx
from features.appointment.dao import AppointmentDAO
from features.service.dao import ServiceDAO
from features.vehicle.dao import VehicleDAO
from features.appointment.schemas import AppointmentCreate, AppointmentUpdate
from features.user.models import User
from common.utils.responses import ErrorMessages

class AppointmentController:
    def __init__(self, db: AsyncSession):
        self.appointment_dao = AppointmentDAO(db)
        self.service_dao = ServiceDAO(db)
        self.vehicle_dao = VehicleDAO(db)

    async def schedule_appointment(self, appointment_in: AppointmentCreate, current_user: User):
        """
        Business Logic:
        1. Verify vehicle existence and ownership.
        2. Fetch official service price if not provided.
        3. Assign current user as cashier if applicable.
        """
        # Ownership check
        vehicle = await self.vehicle_dao.get_by_id(appointment_in.vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found.")
        if current_user.role.name == "Customer" and vehicle.user_id != current_user.id:
            raise HTTPException(status_code=403, detail=ErrorMessages.FORBIDDEN_ROLE)

        # Automatic Price Fetching
        service = await self.service_dao.get_by_id(appointment_in.service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found.")
        appointment_in.total_price = service.cost

        return await self.appointment_dao.create(appointment_in)

    async def get_visible_appointments(self, current_user: User):
        """Filter data based on role (Customer sees theirs, Washer sees theirs, Admin sees all)."""
        if current_user.role.name == "Customer":
            return await self.appointment_dao.get_by_user_id(current_user.id)
        if current_user.role.name == "Washer":
            return await self.appointment_dao.get_by_washer_id(current_user.id)

        return await self.appointment_dao.get_all_with_details()

    async def update_appointment_status(self, appointment_id: int, new_status: str, current_user: User):
        """
        Updates appointment status and automatically sets timestamps.
        Rules:
        - 'In Progress' sets start_time.
        - 'Completed' sets end_time.
        """
        db_appointment = await self.appointment_dao.get_by_id(appointment_id)
        if not db_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")

        # Logic for automated timestamps
        update_data = {"status": new_status}

        if new_status == "In Progress":
            update_data["start_time"] = get_now_mx()
        elif new_status == "Completed":
            update_data["end_time"] = get_now_mx()

        return await self.appointment_dao.update_fields(db_appointment, update_data)