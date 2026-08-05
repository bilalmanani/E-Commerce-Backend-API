import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a raw plain-text password using bcrypt.
    Safely encodes to UTF-8 and enforces bcrypt's 72-byte max length limit.
    """
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a raw plain-text password against a stored bcrypt hash string.
    """
    pwd_bytes = plain_password.encode("utf-8")[:72]
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)
