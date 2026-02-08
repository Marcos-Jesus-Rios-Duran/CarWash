""""
carwash_backend/features/role/models.py
_models for role feature_
"""
from sqlalchemy import Column, Integer, String, Boolean
from common.config.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), unique=True, nullable=False)  # En el pizarrón dice "descripcion", pero un nombre corto es mejor (Admin, Cajero)
    description = Column(String(100), nullable=True)        # Aquí puedes poner la descripción larga
    is_active = Column(Boolean, default=True)               # "estatus"
