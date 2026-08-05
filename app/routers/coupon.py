from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.coupon import CouponCreate, CouponApply, CouponResponse
from app.dependencies.auth import get_current_admin_user, get_current_user
from app.services.coupon import CouponService

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.post("", response_model=CouponResponse, status_code=status.HTTP_201_CREATED)
async def create_coupon(
    coupon_in: CouponCreate,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Create a new promotional discount coupon (Admin only).
    """
    service = CouponService(db)
    return await service.create_coupon(coupon_in)


@router.get("", response_model=List[CouponResponse])
async def list_coupons(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all coupons (Admin only).
    """
    service = CouponService(db)
    return await service.list_coupons(skip=skip, limit=limit)


@router.post("/validate", response_model=CouponResponse)
async def validate_coupon(
    apply_in: CouponApply,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Validate a coupon code for applicability before checkout.
    """
    service = CouponService(db)
    return await service.validate_coupon(apply_in)
