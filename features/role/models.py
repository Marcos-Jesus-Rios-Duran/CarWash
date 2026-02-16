"""
carwash_backend/features/role/models.py
Models for the role feature.
"""

from sqlalchemy import Column, Integer, String, Boolean
from common.config.database import Base


# pylint: disable=too-few-public-methods
class Role(Base):
    """
    Role model representing user permissions levels (e.g., Admin, Cashier).
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Short name for the role (e.g., 'Admin', 'User')
    name = Column(String(60), unique=True, nullable=False)

    # Detailed explanation of what the role can do
    description = Column(String(100), nullable=True)

    # Status to enable or disable the role
    is_active = Column(Boolean, default=True)
