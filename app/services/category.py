from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.repositories.category import CategoryRepository
from app.utils.slug import slugify


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repo = CategoryRepository(db)

    async def create_category(self, cat_in: CategoryCreate) -> Category:
        existing = await self.category_repo.get_by_name(cat_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )

        slug = slugify(cat_in.name)
        data = cat_in.model_dump()
        data["slug"] = slug

        return await self.category_repo.create(data)

    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> Sequence[Category]:
        return await self.category_repo.get_all(skip=skip, limit=limit)

    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category

    async def update_category(self, category_id: int, cat_in: CategoryUpdate) -> Category:
        category = await self.get_category_by_id(category_id)
        update_data = cat_in.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] != category.name:
            existing = await self.category_repo.get_by_name(update_data["name"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category with this name already exists"
                )
            update_data["slug"] = slugify(update_data["name"])

        return await self.category_repo.update(category, update_data)

    async def delete_category(self, category_id: int) -> bool:
        await self.get_category_by_id(category_id)
        return await self.category_repo.delete(category_id)
