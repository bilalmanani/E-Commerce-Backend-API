from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class AddressBase(BaseModel):
    street_address: str = Field(..., min_length=3, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=3, max_length=20)
    country: str = Field("USA", max_length=100)
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street_address: str | None = Field(None, min_length=3, max_length=255)
    city: str | None = Field(None, min_length=2, max_length=100)
    state: str | None = Field(None, min_length=2, max_length=100)
    postal_code: str | None = Field(None, min_length=3, max_length=20)
    country: str | None = Field(None, max_length=100)
    is_default: bool | None = None


class AddressResponse(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
