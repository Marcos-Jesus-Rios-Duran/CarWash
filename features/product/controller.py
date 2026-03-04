"""
Product Controller Module.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from features.product.dao import ProductDAO
from features.product.schemas import ProductCreate, ProductUpdate
from common.utils.responses import ErrorMessages, SuccessMessages

class ProductController:
    def __init__(self, db: AsyncSession):
        self.product_dao = ProductDAO(db)

    async def create_product(self, product_in: ProductCreate):
        return await self.product_dao.create(product_in)

    async def get_all_products(self, include_inactive: bool = False):
        return await self.product_dao.get_all(include_inactive)

    async def get_product_by_id(self, product_id: int):
        product = await self.product_dao.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)
        return product

    async def update_product(self, product_id: int, product_in: ProductUpdate):
        product = await self.product_dao.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)
        return await self.product_dao.update(product, product_in)

    async def delete_product(self, product_id: int):
        product = await self.product_dao.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)
        await self.product_dao.delete(product)
        return {"detail": SuccessMessages.DELETED}