"""
Data Access Object for the product feature.
"""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from features.product.models import Product
from features.product.schemas import ProductCreate, ProductUpdate

class ProductDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product_in: ProductCreate) -> Product:
        new_product = Product(**product_in.model_dump())
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product

    async def get_all(self, include_inactive: bool = False) -> List[Product]:
        query = select(Product)
        if not include_inactive:
            query = query.where(Product.is_active == True)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        query = select(Product).where(Product.id == product_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, db_product: Product, product_in: ProductUpdate) -> Product:
        update_data = product_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product

    async def delete(self, db_product: Product) -> None:
        """Soft delete for products."""
        db_product.is_active = False
        await self.session.commit()