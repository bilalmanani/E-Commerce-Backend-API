from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.dependencies.auth import get_current_user
from app.services.review import ReviewService

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_in: ReviewCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Submit a review and rating for a product.
    """
    service = ReviewService(db)
    return await service.add_review(current_user.id, review_in)


@router.get("/product/{product_id}", response_model=List[ReviewResponse])
async def list_product_reviews(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    List all customer reviews for a given product (Public endpoint).
    """
    service = ReviewService(db)
    return await service.get_product_reviews(product_id, skip=skip, limit=limit)


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_in: ReviewUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update your review rating or comment.
    """
    service = ReviewService(db)
    return await service.update_review(current_user.id, review_id, review_in)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Delete your product review.
    """
    service = ReviewService(db)
    await service.delete_review(current_user.id, review_id)
