from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.repositories.review import ReviewRepository
from app.repositories.product import ProductRepository


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.review_repo = ReviewRepository(db)
        self.product_repo = ProductRepository(db)

    async def add_review(self, user_id: int, review_in: ReviewCreate) -> Review:
        # Validate product
        product = await self.product_repo.get_by_id(review_in.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        # Check if user already reviewed this product
        existing = await self.review_repo.get_user_product_review(user_id, review_in.product_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this product. Use update review endpoint instead."
            )

        data = review_in.model_dump()
        data["user_id"] = user_id
        return await self.review_repo.create(data)

    async def get_product_reviews(self, product_id: int, skip: int = 0, limit: int = 100) -> Sequence[Review]:
        return await self.review_repo.get_product_reviews(product_id, skip=skip, limit=limit)

    async def update_review(self, user_id: int, review_id: int, review_in: ReviewUpdate) -> Review:
        review = await self.review_repo.get_by_id(review_id)
        if not review or review.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        update_data = review_in.model_dump(exclude_unset=True)
        return await self.review_repo.update(review, update_data)

    async def delete_review(self, user_id: int, review_id: int) -> bool:
        review = await self.review_repo.get_by_id(review_id)
        if not review or review.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return await self.review_repo.delete(review_id)
