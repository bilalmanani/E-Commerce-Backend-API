from decimal import Decimal
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_by_id_with_category(self, id: int) -> Product | None:
        """Fetch product with eagerly loaded category."""
        stmt = (
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Product | None:
        stmt = select(Product).where(Product.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def filter_products(
        self,
        search: str | None = None,
        category_id: int | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        sort_by: str | None = "created_at",
        sort_order: str | None = "desc",
        skip: int = 0,
        limit: int = 20
    ) -> tuple[Sequence[Product], int]:
        """
        Advanced query builder: filters by search keyword, category, price range,
        applies dynamic sorting and offset pagination, and eagerly loads categories.
        """
        query = select(Product).options(selectinload(Product.category)).where(Product.is_available == True)

        # 1. Full-text search on title and description
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    Product.title.ilike(search_pattern),
                    Product.description.ilike(search_pattern)
                )
            )

        # 2. Filter by Category ID
        if category_id:
            query = query.where(Product.category_id == category_id)

        # 3. Filter by Price Range
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)

        # Count total matching records before pagination
        count_stmt = select(func.count()).select_from(query.subquery())
        total_count_result = await self.db.execute(count_stmt)
        total_count = total_count_result.scalar_one()

        # 4. Dynamic Sorting
        sort_column = getattr(Product, sort_by, Product.created_at)
        if sort_order and sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # 5. Offset Pagination
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        products = result.scalars().all()

        return products, total_count
