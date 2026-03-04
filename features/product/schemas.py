"""
Pydantic schemas for Product validation and serialization.
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    price: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(default=0, ge=0, description="El stock no puede ser negativo")
    is_active: bool = Field(default=True)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)