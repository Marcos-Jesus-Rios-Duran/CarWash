""""
carwash_backend/features/customer/models.py
_models for customer feature_
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from common.config.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    first_name = Column(String(60), nullable=False)    # "nombre"
    last_name = Column(String(60), nullable=False)     # "papellido" (asumimos estructura similar a user)
    phone_number = Column(String(15), nullable=True)   # "telefono"
    email = Column(String(100), unique=True, nullable=True) # "correo"
    address = Column(String(150), nullable=True)       # "dirección"

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())