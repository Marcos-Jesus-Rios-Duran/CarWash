"""
carwash_backend/features/vehicle/dao.py
_data access object for vehicle feature_
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from features.vehicle.models import Vehicle
from features.vehicle.schemas import VehicleCreate, VehicleUpdate

class VehicleDAO:
    """Handles direct database access for the Vehicle entity."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, vehicle_in: VehicleCreate) -> Vehicle:
        """
        Create a new vehicle record in the database.
        """
        new_vehicle = Vehicle(**vehicle_in.model_dump())
        self.session.add(new_vehicle)
        await self.session.commit()
        await self.session.refresh(new_vehicle)
        return new_vehicle

    async def get_all(self) -> List[Vehicle]:
        """
        Retrieve all vehicles in the system (For Admins and Cashiers).
        """
        query = select(Vehicle)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_owner(self, user_id: int) -> List[Vehicle]:
        """
        Retrieve only the vehicles belonging to a specific user.
        """
        query = select(Vehicle).where(Vehicle.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """Find a vehicle by its ID."""
        query = select(Vehicle).where(Vehicle.id == vehicle_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, db_vehicle: Vehicle, vehicle_in: VehicleUpdate) -> Vehicle:
        """Update the attributes of an existing vehicle."""
        # exclude_unset=True asegura que solo se actualicen los campos que el usuario envió
        update_data = vehicle_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_vehicle, key, value)

        await self.session.commit()
        await self.session.refresh(db_vehicle)
        return db_vehicle

    async def delete(self, db_vehicle: Vehicle) -> None:
        """kill a vehicle record from the database."""
        await self.session.delete(db_vehicle)
        await self.session.commit()