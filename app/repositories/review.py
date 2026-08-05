from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.review import Review
from app.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    def __init__(self, db: AsyncSession):
        super().__init__(Review, db)

    async def get_product_reviews(self, product_id: int, skip: int = 0, limit: int = 100) -> Sequence[Review]:
        stmt = (
            select(Review)
            .options(selectinload(Review.user))
            .where(Review.product_id == product_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_user_product_review(self, user_id: int, product_id: int) -> Review | None:
        stmt = select(Review).where(Review.user_id == user_id, Review.product_id == product_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
