from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: AsyncSession):
        super().__init__(Order, db)

    async def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Order]:
        """Fetch user order history with items, products, and categories loaded."""
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
                selectinload(Order.shipping_address)
            )
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_order_by_id(self, order_id: int, user_id: int | None = None) -> Order | None:
        """Fetch order details by ID (optionally scoped to user_id)."""
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
                selectinload(Order.shipping_address)
            )
            .where(Order.id == order_id)
        )
        if user_id:
            stmt = stmt.where(Order.user_id == user_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
