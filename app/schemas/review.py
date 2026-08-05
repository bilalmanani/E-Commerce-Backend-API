from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import UserResponse


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: str | None = Field(None, max_length=1000)


class ReviewUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    comment: str | None = Field(None, max_length=1000)


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str | None
    created_at: datetime
    updated_at: datetime
    user: UserResponse | None = None
