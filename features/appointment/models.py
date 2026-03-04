"""
carwash_backend/features/appointment/models.py
Models for the appointment feature, managing service schedules and staff.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from common.config.database import Base


# pylint: disable=too-few-public-methods
class Appointment(Base):
    """
    Appointment model representing a car wash service transaction.
    Connects vehicles, services, and staff members.
    """

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Relationships
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    # Involved Staff
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    washer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    vehicle = relationship("Vehicle")
    service = relationship("Service")
    cashier = relationship("User", foreign_keys=[cashier_id])
    washer = relationship("User", foreign_keys=[washer_id])
    # Schedule Information
    appointment_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    # Service Status and Pricing
    status = Column(String(20), default="Pending")
    discount = Column(Float, default=0.0)
    total_price = Column(Float, nullable=False)

    # pylint: disable=not-callable
    created_at = Column(DateTime(timezone=True), server_default=func.now())
