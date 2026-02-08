"""_summary_
carwash_backend/features/vehicle/models.py
_models for vehicle feature_
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from common.config.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Relación con Cliente (Un vehículo pertenece a un cliente)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    plate_number = Column(String(20), unique=True, index=True, nullable=False) # "matricula"
    brand = Column(String(50), nullable=False)  # "Marca" (no está explícito pero es necesario)
    model = Column(String(50), nullable=False)  # "Modelo"
    color = Column(String(30), nullable=True)   # "Color"
    doors = Column(Integer, nullable=True)      # "npuerto"