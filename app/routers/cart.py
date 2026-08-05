from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.dependencies.auth import get_current_user
from app.services.cart import CartService

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])


@router.get("", response_model=CartResponse)
async def get_cart(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    View user shopping cart with item subtotals and total price.
    """
    service = CartService(db)
    return await service.get_user_cart(current_user.id)


@router.post("/items", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def add_item_to_cart(
    item_in: CartItemCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Add product to cart (increments quantity if already in cart).
    """
    service = CartService(db)
    return await service.add_item_to_cart(current_user.id, item_in)


@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item_quantity(
    item_id: int,
    item_in: CartItemUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update quantity of an existing item in the cart.
    """
    service = CartService(db)
    return await service.update_item_quantity(current_user.id, item_id, item_in)


@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_item_from_cart(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Remove an item from the cart.
    """
    service = CartService(db)
    return await service.remove_item_from_cart(current_user.id, item_id)
