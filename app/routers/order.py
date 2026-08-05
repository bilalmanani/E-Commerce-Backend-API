from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.dependencies.auth import get_current_user, get_current_admin_user
from app.services.order import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(
    order_in: OrderCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Checkout & place a new order from cart contents.
    """
    service = OrderService(db)
    return await service.place_order(current_user.id, order_in)


@router.get("", response_model=List[OrderResponse])
async def get_order_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    View user order history.
    """
    service = OrderService(db)
    return await service.get_user_orders(current_user.id, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_details(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Get detailed order breakdown.
    """
    service = OrderService(db)
    return await service.get_order_details(order_id, current_user.id)


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Cancel order & restore product stock.
    """
    service = OrderService(db)
    return await service.cancel_order(order_id, current_user.id)


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update order status (Admin only).
    """
    service = OrderService(db)
    return await service.update_order_status(order_id, status_in)
