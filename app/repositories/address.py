from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.address import Address
from app.repositories.base import BaseRepository


class AddressRepository(BaseRepository[Address]):
    def __init__(self, db: AsyncSession):
        super().__init__(Address, db)

    async def get_user_addresses(self, user_id: int) -> Sequence[Address]:
        stmt = select(Address).where(Address.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id_and_user(self, address_id: int, user_id: int) -> Address | None:
        stmt = select(Address).where(Address.id == address_id, Address.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
