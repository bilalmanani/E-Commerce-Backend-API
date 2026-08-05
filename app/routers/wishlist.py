from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.wishlist import WishlistResponse
from app.dependencies.auth import get_current_user
from app.services.wishlist import WishlistService

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("", response_model=List[WishlistResponse])
async def get_wishlist(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    View user saved wishlist items.
    """
    service = WishlistService(db)
    return await service.get_user_wishlist(current_user.id)


@router.post("/{product_id}", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Save product to user wishlist.
    """
    service = WishlistService(db)
    return await service.add_to_wishlist(current_user.id, product_id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_wishlist(
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Remove product from user wishlist.
    """
    service = WishlistService(db)
    await service.remove_from_wishlist(current_user.id, product_id)
