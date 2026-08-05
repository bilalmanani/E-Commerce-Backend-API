from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.coupon import Coupon
from app.repositories.base import BaseRepository


class CouponRepository(BaseRepository[Coupon]):
    def __init__(self, db: AsyncSession):
        super().__init__(Coupon, db)

    async def get_by_code(self, code: str) -> Coupon | None:
        stmt = select(Coupon).where(Coupon.code == code)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
