"""
carwash_backend/features/vehicle/schemas.py
Pydantic schemas for Vehicle validation and serialization.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# pylint: disable=too-few-public-methods
class VehicleBase(BaseModel):
    """
    Base properties shared by all Vehicle schemas.
    """
    plate_number: str = Field(..., min_length=6, max_length=20, description="Placa del vehículo")
    brand: str = Field(..., min_length=2, max_length=50, description="Marca (ej. Toyota)")
    model: str = Field(..., min_length=2, max_length=50, description="Modelo (ej. Corolla)")
    color: Optional[str] = Field(None, max_length=30)
    doors: Optional[int] = Field(None, ge=1, le=10, description="Número de puertas")


class VehicleCreate(VehicleBase):
    """
    Schema for creating a new Vehicle.
    Requires the user_id to link it to an owner.
    """
    user_id: int


class VehicleUpdate(BaseModel):
    """
    Schema for updating an existing Vehicle.
    All fields are optional to allow partial updates.
    """
    plate_number: Optional[str] = Field(None, min_length=6, max_length=20)
    brand: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = None
    doors: Optional[int] = Field(None, ge=1, le=10)


class VehicleResponse(VehicleBase):
    """
    Schema for sending Vehicle data back to the frontend.
    """
    id: int
    user_id: int

    # Permite que Pydantic lea los datos directamente desde el modelo de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)