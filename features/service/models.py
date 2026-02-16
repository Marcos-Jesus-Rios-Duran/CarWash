"""
carwash_backend/features/service/models.py
Models for the service feature, defining the catalog of available washes.
"""

from sqlalchemy import Column, Integer, String, Boolean, Float
from common.config.database import Base


# pylint: disable=too-few-public-methods
class Service(Base):
    """
    Service model representing a specific car wash type and its base cost.
    """

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Name of the service (e.g., 'Full Wash', 'Interior Cleaning')
    name = Column(String(100), unique=True, nullable=False)

    # Detailed explanation of what the service includes
    description = Column(String(255), nullable=True)

    # Base price for the service
    cost = Column(Float, nullable=False)

    # Status to enable or disable the service in the catalog
    is_active = Column(Boolean, default=True)
