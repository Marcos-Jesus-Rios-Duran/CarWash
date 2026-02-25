"""
carwash_backend/features/auth/schemas.py
Pydantic schemas for Authentication and Token management.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# pylint: disable=too-few-public-methods
class LoginRequest(BaseModel):
    """
    Schema to receive login credentials from the frontend.
    """
    username: str = Field(..., min_length=4, max_length=60)
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    """
    Schema sent to the frontend after a successful login.
    Standard OAuth2 response format.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserTokenBase(BaseModel):
    """
    Base schema for the UserToken database record.
    """
    refresh_token: str
    expires_at: datetime


class UserTokenResponse(UserTokenBase):
    """
    Schema for internal management of tokens or session lists.
    """
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)