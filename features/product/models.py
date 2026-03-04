"""
Models for the isolated product feature.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean
from common.config.database import Base

class Product(Base):
    """
    Product model representing an item for sale.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)