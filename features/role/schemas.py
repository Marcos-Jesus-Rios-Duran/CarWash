"""
carwash_backend/features/role/schemas.py
Pydantic schemas for Role validation and serialization.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# pylint: disable=too-few-public-methods
class RoleBase(BaseModel):
    """
    Base properties shared by all Role schemas.
    """
    name: str = Field(..., min_length=3, max_length=60, description="Nombre del rol (ej. Admin)")
    description: Optional[str] = Field(None, max_length=100, description="Descripción de permisos")
    is_active: bool = Field(default=True)


class RoleCreate(RoleBase):
    """
    Schema for creating a new Role.
    """
    pass


class RoleUpdate(BaseModel):
    """
    Schema for updating an existing Role.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(None, min_length=3, max_length=60)
    description: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class RoleResponse(RoleBase):
    """
    Schema for sending Role data back to the frontend.
    Includes the database ID.
    """
    id: int

    # Configuración para permitir la conversión desde modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)