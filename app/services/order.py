from decimal import Decimal
from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem
from app.models.coupon import Coupon
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.repositories.order import OrderRepository
from app.repositories.cart import CartRepository
from app.repositories.address import AddressRepository
from app.repositories.product import ProductRepository


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.cart_repo = CartRepository(db)
        self.address_repo = AddressRepository(db)
        self.product_repo = ProductRepository(db)

    async def place_order(self, user_id: int, order_in: OrderCreate) -> Order:
        """
        Transactional Checkout Process:
        1. Validate shipping address.
        2. Validate cart items exist.
        3. Check and deduct stock for each product.
        4. Apply optional coupon discount.
        5. Create Order & OrderItem records with frozen purchase prices.
        6. Empty user cart.
        """
        # 1. Validate shipping address
        address = await self.address_repo.get_by_id_and_user(order_in.shipping_address_id, user_id)
        if not address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipping address not found")

        # 2. Retrieve user cart
        cart = await self.cart_repo.get_by_user_id_with_items(user_id)
        if not cart or not cart.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot place an order with an empty cart"
            )

        total_amount = Decimal("0.00")
        order_items_to_create = []

        # 3. Validate and deduct stock per product
        for item in cart.items:
            product = item.product
            if not product.is_available or product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product '{product.title}' has insufficient stock (Only {product.stock} available)"
                )

            # Deduct inventory stock
            product.stock -= item.quantity
            self.db.add(product)

            # Calculate purchase price (freeze current price!)
            unit_price = product.discount_price if product.discount_price else product.price
            subtotal = unit_price * item.quantity
            total_amount += subtotal

            order_items_to_create.append({
                "product_id": product.id,
                "quantity": item.quantity,
                "price_at_purchase": unit_price
            })

        # 4. Apply Coupon Discount if supplied
        if order_in.coupon_code:
            stmt = select(Coupon).where(Coupon.code == order_in.coupon_code, Coupon.is_active == True)
            res = await self.db.execute(stmt)
            coupon = res.scalar_one_or_none()

            if coupon:
                discount = (total_amount * (coupon.discount_percentage / Decimal("100.0")))
                total_amount -= discount

        # 5. Create Order Record
        new_order = Order(
            user_id=user_id,
            shipping_address_id=address.id,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )
        self.db.add(new_order)
        await self.db.flush()  # Obtain new_order.id

        # Create Order Items
        for item_data in order_items_to_create:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price_at_purchase=item_data["price_at_purchase"]
            )
            self.db.add(order_item)

        # 6. Clear user cart items
        stmt_clear = delete(CartItem).where(CartItem.cart_id == cart.id)
        await self.db.execute(stmt_clear)

        # Commit full transaction atomically
        await self.db.commit()

        return await self.order_repo.get_order_by_id(new_order.id, user_id)

    async def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Order]:
        return await self.order_repo.get_user_orders(user_id, skip=skip, limit=limit)

    async def get_order_details(self, order_id: int, user_id: int) -> Order:
        order = await self.order_repo.get_order_by_id(order_id, user_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    async def cancel_order(self, order_id: int, user_id: int) -> Order:
        """
        Cancel order & restore product stock.
        """
        order = await self.order_repo.get_order_by_id(order_id, user_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel an order in '{order.status.value}' status"
            )

        # Restore product stock
        for item in order.items:
            product = await self.product_repo.get_by_id(item.product_id)
            if product:
                product.stock += item.quantity
                self.db.add(product)

        order.status = OrderStatus.CANCELLED
        self.db.add(order)
        await self.db.commit()
        return await self.order_repo.get_order_by_id(order_id, user_id)

    async def update_order_status(self, order_id: int, status_in: OrderStatusUpdate) -> Order:
        order = await self.order_repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        order.status = status_in.status
        self.db.add(order)
        await self.db.commit()
        return await self.order_repo.get_order_by_id(order_id)
