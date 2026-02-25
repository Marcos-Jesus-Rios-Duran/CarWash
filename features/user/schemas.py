"""
carwash_backend/features/user/schemas.py
Pydantic schemas for User validation and serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# pylint: disable=too-few-public-methods
class UserBase(BaseModel):
    """
    Base properties shared by all User schemas.
    """
    first_name: str = Field(..., min_length=1, max_length=60)
    last_name: str = Field(..., min_length=1, max_length=60)
    second_last_name: str = Field(..., min_length=1, max_length=60)
    username: str = Field(..., min_length=4, max_length=60)
    address: Optional[str] = Field(None, max_length=160)
    phone_number: Optional[str] = Field(None, max_length=15)
    email: Optional[EmailStr] = Field(None, max_length=100)
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    Includes the password and the role_id.
    """
    password: str = Field(..., min_length=8, max_length=256)
    role_id: int


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.
    All fields are optional to allow partial updates.
    """
    first_name: Optional[str] = Field(None, max_length=60)
    last_name: Optional[str] = Field(None, max_length=60)
    second_last_name: Optional[str] = Field(None, max_length=60)
    username: Optional[str] = Field(None, max_length=60)
    password: Optional[str] = Field(None, min_length=8, max_length=72)
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=100)
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """
    Schema for sending user data back to the frontend.
    Excludes the password for security.
    """
    id: int
    role_id: int
    created_at: datetime
    updated_at: datetime

    # Permite convertir objetos de SQLAlchemy a Schemas de Pydantic
    model_config = ConfigDict(from_attributes=True)