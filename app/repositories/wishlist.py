from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.wishlist import Wishlist
from app.models.product import Product
from app.repositories.base import BaseRepository


class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self, db: AsyncSession):
        super().__init__(Wishlist, db)

    async def get_user_wishlist(self, user_id: int) -> Sequence[Wishlist]:
        """Fetch user wishlist with eagerly loaded product and category details."""
        stmt = (
            select(Wishlist)
            .options(selectinload(Wishlist.product).selectinload(Product.category))
            .where(Wishlist.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_user_and_product(self, user_id: int, product_id: int) -> Wishlist | None:
        stmt = select(Wishlist).where(
            Wishlist.user_id == user_id,
            Wishlist.product_id == product_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def remove_by_user_and_product(self, user_id: int, product_id: int) -> bool:
        item = await self.get_by_user_and_product(user_id, product_id)
        if item:
            await self.db.delete(item)
            await self.db.commit()
            return True
        return False
