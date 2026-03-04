"""
carwash_backend/features/appointment/schemas.py
Pydantic schemas for Appointment validation and serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# pylint: disable=too-few-public-methods
class AppointmentBase(BaseModel):
    """
    Base properties shared by all Appointment schemas.
    """
    appointment_date: datetime = Field(..., description="Fecha y hora de la cita")
    status: str = Field(default="Pending", max_length=20)
    discount: float = Field(default=0.0, ge=0, description="Descuento aplicado al servicio")
    total_price: Optional[float] = Field(None, ge=0, description="El precio debe ser mayor a 0")


class AppointmentCreate(AppointmentBase):
    """
    Schema for creating a new Appointment.
    Contains the foreign keys required to link the record.
    """
    vehicle_id: int
    service_id: int
    cashier_id: int
    washer_id: Optional[int] = None


class AppointmentUpdate(BaseModel):
    """
    Schema for updating an existing Appointment.
    All fields are optional to allow partial updates (PATCH).
    """
    appointment_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)
    washer_id: Optional[int] = None
    total_price: Optional[float] = Field(None, gt=0)


class AppointmentResponse(AppointmentBase):
    """
    Schema for sending Appointment data back to the frontend.
    Includes the database ID and timestamps.
    """
    id: int
    vehicle_id: int
    service_id: int
    cashier_id: int
    washer_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime

    # Pydantic V2 configuration to allow working with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

class AppointmentDailyReport(BaseModel):
    """
    Schema for the comprehensive daily report requested by management.
    """
    appointment_id: int
    status: str
    cashier_full_name: str
    washer_full_name: str
    service_name: str
    service_description: Optional[str]
    service_cost: float
    discount: float
    total_price: float
    vehicle_plate: str
    vehicle_brand: str
    vehicle_model: str
    vehicle_color: Optional[str]
    duration_minutes: Optional[int] = Field(None, description="Tiempo que tardó el lavador en minutos")

    model_config = ConfigDict(from_attributes=True)
