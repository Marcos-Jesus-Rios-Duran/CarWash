""""
carwash_backend/features/service/dao.py
_data access object for service feature_
"""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from features.service.models import Service
from features.service.schemas import ServiceCreate, ServiceUpdate

class ServiceDAO:
    """Handles direct database access for the Service entity."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, service_in: ServiceCreate) -> Service:
        """Create a new service in the catalog."""
        new_service = Service(**service_in.model_dump())
        self.session.add(new_service)
        await self.session.commit()
        await self.session.refresh(new_service)
        return new_service

    async def get_all_active(self) -> List[Service]:
        """Retrieve all services where is_active is True."""
        query = select(Service).where(Service.is_active == True)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, service_id: int) -> Optional[Service]:
        """Fetch a specific service by its ID."""
        query = select(Service).where(Service.id == service_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, db_service: Service, service_in: ServiceUpdate) -> Service:
        """Update service details like price or description."""
        update_data = service_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_service, key, value)
        await self.session.commit()
        await self.session.refresh(db_service)
        return db_service

    async def delete(self, db_service: Service) -> None:
        """Soft delete: Sets is_active to False to preserve historical data."""
        db_service.is_active = False
        await self.session.commit()