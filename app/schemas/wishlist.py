from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.product import ProductResponse


class WishlistCreate(BaseModel):
    product_id: int


class WishlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    created_at: datetime
    product: ProductResponse | None = None
