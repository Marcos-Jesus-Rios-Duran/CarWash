"""""
carwash_backend/features/service/models.py
_models for service feature_
"""
from sqlalchemy import Column, Integer, String, Boolean, Float
from common.config.database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False) # "nombre"
    description = Column(String(255), nullable=True)        # "descripcion"
    cost = Column(Float, nullable=False)                    # "Costo"

    is_active = Column(Boolean, default=True)