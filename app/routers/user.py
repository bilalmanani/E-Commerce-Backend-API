from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, PasswordChange
from app.dependencies.auth import get_current_user, get_current_admin_user
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Fetch profile information of the currently logged-in user.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update profile information (first_name, last_name, email).
    """
    service = UserService(db)
    return await service.update_profile(current_user, user_in)


@router.post("/me/change-password")
async def change_password(
    pwd_in: PasswordChange,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Change account password (requires verifying current password).
    """
    service = UserService(db)
    await service.change_password(current_user, pwd_in)
    return {"message": "Password changed successfully"}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Delete the currently logged-in user's account.
    """
    service = UserService(db)
    await service.delete_account(current_user.id)


@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all users (Admin only privilege).
    """
    service = UserService(db)
    return await service.list_all_users(skip=skip, limit=limit)
