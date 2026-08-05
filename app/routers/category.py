from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.dependencies.auth import get_current_admin_user
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    cat_in: CategoryCreate,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Create a new product category (Admin only).
    """
    service = CategoryService(db)
    return await service.create_category(cat_in)


@router.get("", response_model=List[CategoryResponse])
async def list_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    List all active categories (Public endpoint).
    """
    service = CategoryService(db)
    return await service.get_all_categories(skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single category by ID (Public endpoint).
    """
    service = CategoryService(db)
    return await service.get_category_by_id(category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    cat_in: CategoryUpdate,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update a category (Admin only).
    """
    service = CategoryService(db)
    return await service.update_category(category_id, cat_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Delete a category (Admin only).
    """
    service = CategoryService(db)
    await service.delete_category(category_id)
