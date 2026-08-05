from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class CouponCreate(BaseModel):
    code: str = Field(..., min_length=3, max_length=50)
    discount_percentage: Decimal = Field(..., gt=0, le=100)
    valid_from: datetime
    valid_until: datetime


class CouponApply(BaseModel):
    code: str


class CouponResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    discount_percentage: Decimal
    valid_from: datetime
    valid_until: datetime
    is_active: bool
    created_at: datetime
