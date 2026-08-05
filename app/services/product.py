from decimal import Decimal
from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository
from app.utils.slug import slugify


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)

    async def create_product(self, prod_in: ProductCreate) -> Product:
        # Validate category existence
        category = await self.category_repo.get_by_id(prod_in.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        slug = slugify(prod_in.title)
        existing_slug = await self.product_repo.get_by_slug(slug)
        if existing_slug:
            slug = f"{slug}-{int(prod_in.price)}"

        data = prod_in.model_dump()
        data["slug"] = slug

        created_product = await self.product_repo.create(data)
        
        # Eagerly load category before returning for response serialization
        return await self.product_repo.get_by_id_with_category(created_product.id)

    async def get_product(self, product_id: int) -> Product:
        product = await self.product_repo.get_by_id_with_category(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    async def list_products(
        self,
        search: str | None = None,
        category_id: int | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 20
    ):
        products, total_count = await self.product_repo.filter_products(
            search=search,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit
        )
        return {
            "items": products,
            "total": total_count,
            "skip": skip,
            "limit": limit
        }

    async def update_product(self, product_id: int, prod_in: ProductUpdate) -> Product:
        product = await self.get_product(product_id)
        update_data = prod_in.model_dump(exclude_unset=True)

        if "category_id" in update_data and update_data["category_id"] is not None:
            category = await self.category_repo.get_by_id(update_data["category_id"])
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        if "title" in update_data and update_data["title"] != product.title:
            update_data["slug"] = slugify(update_data["title"])

        await self.product_repo.update(product, update_data)
        return await self.product_repo.get_by_id_with_category(product_id)

    async def delete_product(self, product_id: int) -> bool:
        await self.get_product(product_id)
        return await self.product_repo.delete(product_id)
