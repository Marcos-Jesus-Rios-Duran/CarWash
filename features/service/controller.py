"""
Service Controller Module.
Manages business logic for the car wash service catalog.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from features.service.dao import ServiceDAO
from features.service.schemas import ServiceCreate, ServiceUpdate
from common.utils.responses import ErrorMessages

class ServiceController:
    """Business logic layer for service management."""

    def __init__(self, db: AsyncSession):
        self.service_dao = ServiceDAO(db)

    async def add_service(self, service_in: ServiceCreate):
        """Adds a service ensuring the name is unique."""
        try:
            return await self.service_dao.create(service_in)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A service with this name already exists."
            )

    async def get_catalog(self):
        """Returns the list of all available services."""
        return await self.service_dao.get_all_active()

    async def modify_service(self, service_id: int, service_in: ServiceUpdate):
        """Updates an existing service in the catalog."""
        db_service = await self.service_dao.get_by_id(service_id)
        if not db_service:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)

        return await self.service_dao.update(db_service, service_in)

    async def remove_service(self, service_id: int):
        """Deactivates a service from the catalog."""
        db_service = await self.service_dao.get_by_id(service_id)
        if not db_service:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)

        await self.service_dao.delete(db_service)
        return {"detail": "Service deactivated successfully."}