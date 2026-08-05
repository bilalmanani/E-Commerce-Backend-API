from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.token import TokenData


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a short-lived JWT Access Token.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a long-lived JWT Refresh Token.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, expected_type: str = "access") -> TokenData | None:
    """
    Decode and validate JWT signature and payload.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        token_type: str = payload.get("type")

        if user_id is None or token_type != expected_type:
            return None

        return TokenData(user_id=int(user_id), email=email, role=role)
    except JWTError:
        return None
