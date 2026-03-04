"""
Routes for product feature (Unprotected).
"""
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.config.database import get_db
from features.product.schemas import ProductCreate, ProductResponse, ProductUpdate
from features.product.controller import ProductController

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new product."""
    controller = ProductController(db)
    return await controller.create_product(product)

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    include_inactive: bool = Query(False, description="Include deactivated products in the list"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves all products."""
    controller = ProductController(db)
    return await controller.get_all_products(include_inactive)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieves a specific product by ID."""
    controller = ProductController(db)
    return await controller.get_product_by_id(product_id)

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_in: ProductUpdate, db: AsyncSession = Depends(get_db)):
    """Updates an existing product."""
    controller = ProductController(db)
    return await controller.update_product(product_id, product_in)

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Soft-deletes a product."""
    controller = ProductController(db)
    return await controller.delete_product(product_id)