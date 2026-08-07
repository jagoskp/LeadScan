import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from leadscan_config import AppSettings

logger = logging.getLogger("leadscan-security")
settings = AppSettings()
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plain text password using Argon2id algorithm."""
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a stored Argon2 hash."""
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except Exception as e:
        logger.error("Error during password verification: %s", e)
        return False


def create_jwt_token(
    subject: str,
    expires_delta: timedelta,
    token_type: str = "access",
) -> str:
    """Generate a JWT token for the given subject (e.g. user_id)."""
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    payload = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "type": token_type,
        "jti": uuid.uuid4().hex,
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_jwt_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token signature is invalid.
    """
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
