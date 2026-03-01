""""
carwash_backend/features/service/routes.py
_routes for service feature_
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.config.database import get_db
from common.security.permissions import RoleChecker
from features.service.schemas import ServiceCreate, ServiceResponse, ServiceUpdate
from features.service.controller import ServiceController

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    service: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    _ = Depends(RoleChecker(["Admin"]))
):
    """Adds a new service to the catalog. Admin only."""
    controller = ServiceController(db)
    return await controller.add_service(service)

@router.get("/", response_model=List[ServiceResponse])
async def list_services(db: AsyncSession = Depends(get_db)):
    """Public catalog of available services."""
    controller = ServiceController(db)
    return await controller.get_catalog()

@router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    _ = Depends(RoleChecker(["Admin"]))
):
    """Updates service price or description. Admin only."""
    controller = ServiceController(db)
    return await controller.modify_service(service_id, service)

@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    _ = Depends(RoleChecker(["Admin"]))
):
    """Deactivates a service. Admin only."""
    controller = ServiceController(db)
    return await controller.remove_service(service_id)