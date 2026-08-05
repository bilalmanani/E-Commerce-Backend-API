from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.session import get_db
from app.models.user import User, UserRole
from app.models.cart import Cart
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, RefreshTokenRequest
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token, verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Register a new user account and initialize an empty shopping cart.
    """
    # 1. Check if user already exists
    stmt = select(User).where(User.email == user_in.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # 2. Hash raw password
    hashed_pwd = hash_password(user_in.password)

    # 3. Create User object (Public registration is always customer role for security)
    new_user = User(
        email=user_in.email.strip().lower(),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=hashed_pwd,
        role=UserRole.CUSTOMER
    )
    db.add(new_user)
    await db.flush()  # Populates new_user.id before commit

    # 4. Initialize an empty shopping cart for the user
    new_cart = Cart(user_id=new_user.id)
    db.add(new_cart)

    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    OAuth2 compatible token login, returning Access & Refresh Tokens.
    """
    clean_username = form_data.username.strip().lower() if form_data.username else ""
    stmt = select(User).where(func.lower(User.email) == clean_username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )

    token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_in: RefreshTokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Generate a new access token using a valid refresh token.
    """
    token_data = verify_token(refresh_in.refresh_token, expected_type="refresh")
    if not token_data or not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    stmt = select(User).where(User.id == token_data.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    new_data = {"sub": str(user.id), "email": user.email, "role": user.role}
    new_access_token = create_access_token(data=new_data)
    new_refresh_token = create_refresh_token(data=new_data)

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout():
    """
    Logout endpoint (Client discards tokens).
    """
    return {"message": "Successfully logged out. Please clear tokens from client storage."}
