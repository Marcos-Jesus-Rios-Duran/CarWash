"""
carwash_backend/features/vehicle/models.py
Models for the vehicle feature, representing car details and ownership.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from common.config.database import Base


# pylint: disable=too-few-public-methods
class Vehicle(Base):
    """
    Vehicle model representing a car registered in the system.
    Linked to a specific customer through a foreign key.
    """

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Customer Relationship (One vehicle belongs to one customer)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # Vehicle Specifications
    plate_number = Column(String(20), unique=True, index=True, nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    color = Column(String(30), nullable=True)
    doors = Column(Integer, nullable=True)
