from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.repositories.address import AddressRepository


class AddressService:
    def __init__(self, db: AsyncSession):
        self.address_repo = AddressRepository(db)

    async def create_address(self, user_id: int, addr_in: AddressCreate) -> Address:
        data = addr_in.model_dump()
        data["user_id"] = user_id
        return await self.address_repo.create(data)

    async def get_user_addresses(self, user_id: int) -> Sequence[Address]:
        return await self.address_repo.get_user_addresses(user_id)

    async def get_address(self, address_id: int, user_id: int) -> Address:
        addr = await self.address_repo.get_by_id_and_user(address_id, user_id)
        if not addr:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        return addr

    async def delete_address(self, address_id: int, user_id: int) -> bool:
        await self.get_address(address_id, user_id)
        return await self.address_repo.delete(address_id)
