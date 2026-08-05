from decimal import Decimal
from typing import Annotated, List, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database.session import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.dependencies.auth import get_current_admin_user
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


class PaginatedProductResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    skip: int
    limit: int


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    prod_in: ProductCreate,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Create a new product (Admin only).
    """
    service = ProductService(db)
    return await service.create_product(prod_in)


@router.get("", response_model=PaginatedProductResponse)
async def list_products(
    search: str | None = Query(None, description="Search products by title or description"),
    category_id: int | None = Query(None, description="Filter by Category ID"),
    min_price: Decimal | None = Query(None, description="Minimum price threshold"),
    max_price: Decimal | None = Query(None, description="Maximum price threshold"),
    sort_by: str = Query("created_at", description="Field to sort by (price, title, created_at)"),
    sort_order: str = Query("desc", description="Sort direction (asc, desc)"),
    skip: int = Query(0, ge=0, description="Offset pagination skip"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    List, search, filter, sort, and paginate products (Public endpoint).
    """
    service = ProductService(db)
    return await service.list_products(
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get product details by ID (Public endpoint).
    """
    service = ProductService(db)
    return await service.get_product(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    prod_in: ProductUpdate,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update a product (Admin only).
    """
    service = ProductService(db)
    return await service.update_product(product_id, prod_in)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Delete a product (Admin only).
    """
    service = ProductService(db)
    await service.delete_product(product_id)
