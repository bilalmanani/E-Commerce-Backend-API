from datetime import datetime, timezone
from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponApply, CouponResponse
from app.repositories.coupon import CouponRepository


class CouponService:
    def __init__(self, db: AsyncSession):
        self.coupon_repo = CouponRepository(db)

    async def create_coupon(self, coupon_in: CouponCreate) -> Coupon:
        existing = await self.coupon_repo.get_by_code(coupon_in.code.upper())
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon code already exists"
            )

        data = coupon_in.model_dump()
        data["code"] = coupon_in.code.upper()
        return await self.coupon_repo.create(data)

    async def list_coupons(self, skip: int = 0, limit: int = 100) -> Sequence[Coupon]:
        return await self.coupon_repo.get_all(skip=skip, limit=limit)

    async def validate_coupon(self, apply_in: CouponApply) -> Coupon:
        coupon = await self.coupon_repo.get_by_code(apply_in.code.upper())
        if not coupon or not coupon.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid or inactive coupon code"
            )

        now = datetime.now(timezone.utc)
        if coupon.valid_from > now or coupon.valid_until < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon code has expired or is not yet active"
            )

        return coupon
