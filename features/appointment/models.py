"""""
carwash_backend/features/appointment/models.py
_models for appointment feature_
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from common.config.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    #
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False) # "Id_vehiculo"
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False) # "Id_servicio"

    # Empleados involucrados
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False) # "Id_cajero"
    washer_id = Column(Integer, ForeignKey("users.id"), nullable=True)   # "Id_lavador"

    # Fechas y Horas
    appointment_date = Column(DateTime, nullable=False) # "Fecha"
    start_time = Column(DateTime, nullable=True)        # "horain"
    end_time = Column(DateTime, nullable=True)          # "horafin"

    status = Column(String(20), default="Pending")      # Estado del servicio
    total_price = Column(Float, nullable=False)         # Precio final (puede variar del costo base)

    created_at = Column(DateTime(timezone=True), server_default=func.now())