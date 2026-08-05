from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.address import AddressCreate, AddressResponse
from app.dependencies.auth import get_current_user
from app.services.address import AddressService

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(
    addr_in: AddressCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Add a new shipping address.
    """
    service = AddressService(db)
    return await service.create_address(current_user.id, addr_in)


@router.get("", response_model=List[AddressResponse])
async def list_addresses(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    List user shipping addresses.
    """
    service = AddressService(db)
    return await service.get_user_addresses(current_user.id)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Delete a shipping address.
    """
    service = AddressService(db)
    await service.delete_address(address_id, current_user.id)
