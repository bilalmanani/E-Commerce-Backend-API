from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.product import ProductResponse


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1, description="Quantity must be at least 1")


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cart_id: int
    product_id: int
    quantity: int
    product: ProductResponse
    subtotal: Decimal | None = None


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    items: List[CartItemResponse] = []
    total_price: Decimal = Decimal("0.00")
