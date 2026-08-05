from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from app.schemas.category import CategoryResponse


class ProductBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=10)
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Price must be greater than 0")
    discount_price: Decimal | None = Field(None, decimal_places=2)
    stock: int = Field(..., ge=0)
    is_available: bool = True
    image_url: str | None = None
    category_id: int

    @model_validator(mode="after")
    def validate_discount_price(self):
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("discount_price must be less than regular price")
        return self


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: str | None = Field(None, min_length=2, max_length=255)
    description: str | None = Field(None, min_length=10)
    price: Decimal | None = Field(None, gt=0)
    discount_price: Decimal | None = Field(None)
    stock: int | None = Field(None, ge=0)
    is_available: bool | None = None
    image_url: str | None = None
    category_id: int | None = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    category: CategoryResponse | None = None
