from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart import Cart
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse


class CartService:
    def __init__(self, db: AsyncSession):
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_user_cart(self, user_id: int) -> CartResponse:
        cart = await self.cart_repo.get_by_user_id_with_items(user_id)
        if not cart:
            # Create cart if missing
            cart = await self.cart_repo.create({"user_id": user_id})
            cart = await self.cart_repo.get_by_user_id_with_items(user_id)

        # Compute subtotals and total price dynamically
        items_response = []
        total_price = Decimal("0.00")

        if cart and cart.items:
            for item in cart.items:
                price = item.product.discount_price if item.product.discount_price else item.product.price
                subtotal = price * item.quantity
                total_price += subtotal

                item_resp = CartItemResponse(
                    id=item.id,
                    cart_id=item.cart_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    product=item.product,
                    subtotal=subtotal
                )
                items_response.append(item_resp)

        return CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            items=items_response,
            total_price=total_price
        )

    async def add_item_to_cart(self, user_id: int, item_in: CartItemCreate) -> CartResponse:
        # 1. Validate Product Existence & Stock
        product = await self.product_repo.get_by_id(item_in.product_id)
        if not product or not product.is_available:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not available")

        if product.stock < item_in.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Requested quantity exceeds available stock ({product.stock} available)"
            )

        # 2. Get or create cart
        cart = await self.cart_repo.get_by_user_id_with_items(user_id)
        if not cart:
            cart = await self.cart_repo.create({"user_id": user_id})

        # 3. Add or update item
        await self.cart_repo.add_or_update_item(cart.id, item_in.product_id, item_in.quantity)
        return await self.get_user_cart(user_id)

    async def update_item_quantity(self, user_id: int, item_id: int, item_in: CartItemUpdate) -> CartResponse:
        cart = await self.cart_repo.get_by_user_id_with_items(user_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

        updated_item = await self.cart_repo.update_item_quantity(item_id, cart.id, item_in.quantity)
        if not updated_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

        return await self.get_user_cart(user_id)

    async def remove_item_from_cart(self, user_id: int, item_id: int) -> CartResponse:
        cart = await self.cart_repo.get_by_user_id_with_items(user_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

        deleted = await self.cart_repo.remove_item(item_id, cart.id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

        return await self.get_user_cart(user_id)
