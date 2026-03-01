"""
Vehicle Controller Module.
Handles business logic and authorization rules for vehicles.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError # Importamos esto para atrapar el error de la placa

from common.utils.responses import ErrorMessages, SuccessMessages
from features.vehicle.dao import VehicleDAO
from features.vehicle.schemas import VehicleCreate, VehicleUpdate
from features.user.models import User

class VehicleController:
    """Business logic layer for managing vehicles."""

    def __init__(self, db: AsyncSession):
        self.vehicle_dao = VehicleDAO(db)

    async def register_vehicle(self, vehicle_in: VehicleCreate, current_user: User):
        """
        Registers a vehicle applying ownership rules.
        """
        if current_user.role.name == "Customer":
            vehicle_in.user_id = current_user.id

        try:
            return await self.vehicle_dao.create(vehicle_in)
        except IntegrityError:
            # Si SQLAlchemy detecta que la placa ya existe, lanzamos un 400
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un vehículo registrado con ese número de placa."
            )

    async def get_allowed_vehicles(self, current_user: User):
        """
        Returns vehicles based on the user's role.
        """
        if current_user.role.name == "Customer":
            return await self.vehicle_dao.get_by_owner(current_user.id)

        return await self.vehicle_dao.get_all()
    async def update_vehicle(self, vehicle_id: int, vehicle_in: VehicleUpdate, current_user: User):
        """Aplica reglas de negocio para actualizar un vehículo."""
        vehicle = await self.vehicle_dao.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)

        # Regla de seguridad: Si es Customer, el vehículo debe ser suyo
        if current_user.role.name == "Customer" and vehicle.user_id != current_user.id:
            raise HTTPException(status_code=403, detail=ErrorMessages.FORBIDDEN_ROLE)

        # Usamos el try/except por si intenta actualizar a una placa que ya existe
        try:
            return await self.vehicle_dao.update(vehicle, vehicle_in)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un vehículo registrado con ese número de placa."
            )

    async def delete_vehicle(self, vehicle_id: int, current_user: User):
        """Aplica reglas de negocio para eliminar un vehículo."""
        vehicle = await self.vehicle_dao.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)

        # Regla de seguridad: Si es Customer, el vehículo debe ser suyo
        if current_user.role.name == "Customer" and vehicle.user_id != current_user.id:
            raise HTTPException(status_code=403, detail=ErrorMessages.FORBIDDEN_ROLE)

        await self.vehicle_dao.delete(vehicle)
        return {"detail": SuccessMessages.DELETED}