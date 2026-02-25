"""
carwash_backend/features/user/schemas.py
Pydantic schemas for User validation and serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """
    Base properties shared by all User schemas.
    """
    first_name: str = Field(..., min_length=1, max_length=60)
    last_name: str = Field(..., min_length=1, max_length=60)
    second_last_name: str = Field(..., min_length=1, max_length=60)
    username: str = Field(..., min_length=4, max_length=60)
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=100)
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    Allows passing a role_name string instead of a technical ID.
    """
    # limit to  72 characters to prevent bcrypt issues (72 is the max for bcrypt)
    password: str = Field(..., min_length=8, max_length=72)

    # role_name is a user-friendly way to specify the role during registration.
    role_name: str = Field(default="Customer", description="Nombre del rol a asignar")

    # role_id optional for backward compatibility, but will be ignored if role_name is provided.
    role_id: Optional[int] = None


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.
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
    """
    id: int
    role_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)