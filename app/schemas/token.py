from pydantic import BaseModel
from app.models.user import UserRole


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None
    role: UserRole | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
