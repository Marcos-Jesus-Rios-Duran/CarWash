"""
Role models for the CarWash system.
Defines permission levels for different user types.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from common.config.database import Base


class Role(Base):
    """
    Role model representing permission levels.
    Examples: 'Admin', 'Cashier', 'Washer', 'Customer'.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60), unique=True, nullable=False)
    description = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)

    # Bidirectional relationship with User
    users = relationship("User", back_populates="role")