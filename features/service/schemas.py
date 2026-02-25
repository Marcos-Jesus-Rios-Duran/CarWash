"""
carwash_backend/features/service/schemas.py
Pydantic schemas for Service validation and serialization.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# pylint: disable=too-few-public-methods
class ServiceBase(BaseModel):
    """
    Base properties shared by all Service schemas.
    """
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del servicio")
    description: Optional[str] = Field(None, max_length=255, description="Detalles de lo que incluye")
    cost: float = Field(..., gt=0, description="El costo debe ser mayor a 0")
    is_active: bool = Field(default=True)


class ServiceCreate(ServiceBase):
    """
    Schema for creating a new Service in the catalog.
    """
    pass


class ServiceUpdate(BaseModel):
    """
    Schema for updating an existing Service.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    cost: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class ServiceResponse(ServiceBase):
    """
    Schema for sending Service data back to the frontend.
    Includes the database ID.
    """
    id: int

    # Configuración para permitir la conversión desde modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)