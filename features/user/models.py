"""
carwash_backend/features/user/models.py
SQLAlchemy model definition for the User feature.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from common.config.database import Base
from common.utils.date_utils import get_now_mx  # <--- Importamos nuestra utilidad

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # --- Personal Info (Mexican Style) ---
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)       # Apellido Paterno
    # AQUI: Al poner nullable=False, la base de datos RECHAZARÁ si va vacío.
    second_last_name = Column(String(60), nullable=False) # Apellido Materno (Obligatorio)

    username = Column(String(60), unique=True, index=True, nullable=False)
    password = Column(String(256), nullable=False)

    address = Column(String(160), nullable=True)
    phone_number = Column(String(15), nullable=True)
    email = Column(String(100), unique=True, nullable=True)

    is_active = Column(Boolean, default=True)

    # --- Fechas con Hora de México ---
    # Usamos 'default' (Python) en vez de 'server_default' (SQL)
    # para garantizar que se guarde con la hora que calculamos en utils.
    created_at = Column(DateTime(timezone=True), default=get_now_mx)
    updated_at = Column(DateTime(timezone=True), default=get_now_mx, onupdate=get_now_mx)