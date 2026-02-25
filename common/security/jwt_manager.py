import jwt
from datetime import datetime, timedelta, timezone
from common.config.config import get_settings

settings = get_settings()

def create_access_token(data: dict) -> str:
    """
    Generates a signed JWT access token.

    Args:
        data (dict): The payload to include in the token (e.g., user_id, role).

    Returns:
        str: The encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    """
    Decodes and validates a JWT access token.

    Args:
        token (str): The JWT string to decode.

    Returns:
        dict: The decoded payload if valid.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is malformed or invalid.
    """
    # We let the exceptions propagate so the caller (Security Dependency)
    # can catch them and raise specific FastAPI HTTPExceptions.
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])