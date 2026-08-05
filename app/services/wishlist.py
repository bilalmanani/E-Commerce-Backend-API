from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wishlist import Wishlist
from app.repositories.wishlist import WishlistRepository
from app.repositories.product import ProductRepository


class WishlistService:
    def __init__(self, db: AsyncSession):
        self.wishlist_repo = WishlistRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_user_wishlist(self, user_id: int) -> Sequence[Wishlist]:
        return await self.wishlist_repo.get_user_wishlist(user_id)

    async def add_to_wishlist(self, user_id: int, product_id: int) -> Wishlist:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        existing = await self.wishlist_repo.get_by_user_and_product(user_id, product_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is already in your wishlist"
            )

        return await self.wishlist_repo.create({"user_id": user_id, "product_id": product_id})

    async def remove_from_wishlist(self, user_id: int, product_id: int) -> bool:
        removed = await self.wishlist_repo.remove_by_user_and_product(user_id, product_id)
        if not removed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist item not found")
        return True
