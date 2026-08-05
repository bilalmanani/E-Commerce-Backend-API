from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from app.models.order import OrderStatus
from app.schemas.address import AddressResponse
from app.schemas.product import ProductResponse


class OrderCreate(BaseModel):
    shipping_address_id: int
    coupon_code: str | None = None


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal
    product: ProductResponse | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    shipping_address_id: int | None
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    shipping_address: AddressResponse | None = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
