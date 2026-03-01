"""""
carwash_backend/features/appointment/dao.py
_data access object for appointment feature_
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from features.appointment.models import Appointment
from features.appointment.schemas import AppointmentCreate, AppointmentUpdate

class AppointmentDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, appointment_in: AppointmentCreate) -> Appointment:
        """Persists a new appointment in the database."""
        new_appointment = Appointment(**appointment_in.model_dump())
        self.session.add(new_appointment)
        await self.session.commit()
        await self.session.refresh(new_appointment)
        return new_appointment

    async def get_all_with_details(self) -> List[Appointment]:
        """Retrieves all appointments with related vehicle and service data."""
        query = select(Appointment).options(
            selectinload(Appointment.vehicle),
            selectinload(Appointment.service),
            selectinload(Appointment.washer)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Finds a specific appointment by ID."""
        query = select(Appointment).where(Appointment.id == appointment_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_user_id(self, user_id: int) -> List[Appointment]:
        """Retrieves history for a specific customer (via their vehicles)."""
        from features.vehicle.models import Vehicle
        query = select(Appointment).join(Vehicle).where(Vehicle.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_washer_id(self, washer_id: int) -> List[Appointment]:
        """Retrieves appointments assigned to a specific washer."""
        query = select(Appointment).where(Appointment.washer_id == washer_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_status(self, db_appointment: Appointment, status: str) -> Appointment:
        """Updates only the status of the service."""
        db_appointment.status = status
        await self.session.commit()
        await self.session.refresh(db_appointment)
        return db_appointment

    async def update_fields(self, db_obj: Appointment, update_data: dict) -> Appointment:
        """
        Generic method to update multiple fields of an appointment.
        Useful for automated timestamps (start_time, end_time) and status changes.
        """
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj