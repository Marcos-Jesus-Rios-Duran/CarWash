"""
carwash_backend/features/auth/models.py
Models for auth feature (Refresh Tokens).
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from common.config.database import Base
from common.utils.date_utils import get_now_mx

class UserToken(Base):
    """
    Tabla para gestionar Refresh Tokens.
    Permite mantener sesiones abiertas o revocarlas forzosamente.
    """
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # El token real (generalmente un hash o string largo)
    refresh_token = Column(String(255), unique=True, index=True, nullable=False)

    # Fecha de expiración del token
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_now_mx)

    user = relationship("User")