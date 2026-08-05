from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserUpdate, PasswordChange
from app.repositories.user import UserRepository
from app.auth.security import verify_password, hash_password


class UserService:
    """
    Business logic layer for User operations.
    """

    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def get_profile(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_profile(self, user: User, user_in: UserUpdate) -> User:
        # Check email uniqueness if email is being updated
        if user_in.email and user_in.email != user.email:
            existing = await self.user_repo.get_by_email(user_in.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already in use by another account"
                )

        update_data = user_in.model_dump(exclude_unset=True)
        return await self.user_repo.update(user, update_data)

    async def change_password(self, user: User, pwd_in: PasswordChange) -> bool:
        # Verify current password
        if not verify_password(pwd_in.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )

        new_hashed_password = hash_password(pwd_in.new_password)
        await self.user_repo.update(user, {"hashed_password": new_hashed_password})
        return True

    async def delete_account(self, user_id: int) -> bool:
        return await self.user_repo.delete(user_id)

    async def list_all_users(self, skip: int = 0, limit: int = 100):
        return await self.user_repo.get_all(skip=skip, limit=limit)
