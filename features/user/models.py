"""
User models for the CarWash system.
Handles personal information, authentication, and role assignment.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from common.config.database import Base
from common.utils.date_utils import get_now_mx


class User(Base):
    """
    User model containing profile data and security credentials.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # Names based on Mexican naming conventions
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)          # Paternal Surname
    second_last_name = Column(String(60), nullable=False)   # Maternal Surname

    username = Column(String(60), unique=True, index=True, nullable=False)
    password = Column(String(256), nullable=False)

    address = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, nullable=False)

    is_active = Column(Boolean, default=True)

    # Relationships
    role = relationship("Role", back_populates="users")
    vehicles = relationship("Vehicle", back_populates="owner")

    # Timestamps with Mexico City timezone
    created_at = Column(DateTime(timezone=True), default=get_now_mx)
    updated_at = Column(DateTime(timezone=True), default=get_now_mx, onupdate=get_now_mx)