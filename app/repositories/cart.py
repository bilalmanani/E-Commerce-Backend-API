from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.repositories.base import BaseRepository


class CartRepository(BaseRepository[Cart]):
    def __init__(self, db: AsyncSession):
        super().__init__(Cart, db)

    async def get_by_user_id_with_items(self, user_id: int) -> Cart | None:
        """
        Fetch user cart eagerly loading cart items, product details, and category.
        """
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.product)
                .selectinload(Product.category)
            )
            .where(Cart.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_cart_item(self, cart_id: int, product_id: int) -> CartItem | None:
        """Find specific item inside user cart."""
        stmt = select(CartItem).where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def add_or_update_item(self, cart_id: int, product_id: int, quantity: int) -> CartItem:
        """Add new item or increment quantity if product already exists in cart."""
        existing_item = await self.get_cart_item(cart_id, product_id)
        if existing_item:
            existing_item.quantity += quantity
            self.db.add(existing_item)
            await self.db.commit()
            await self.db.refresh(existing_item)
            return existing_item

        new_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self.db.add(new_item)
        await self.db.commit()
        await self.db.refresh(new_item)
        return new_item

    async def update_item_quantity(self, item_id: int, cart_id: int, new_quantity: int) -> CartItem | None:
        stmt = select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart_id)
        result = await self.db.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            item.quantity = new_quantity
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
        return item

    async def remove_item(self, item_id: int, cart_id: int) -> bool:
        stmt = select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart_id)
        result = await self.db.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            await self.db.delete(item)
            await self.db.commit()
            return True
        return False
