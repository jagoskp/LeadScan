import uuid
from typing import AsyncGenerator
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.database import get_db
from services.api.src.auth.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
    UserInactiveException,
)
from services.api.src.auth.models import User
from services.api.src.auth.repository import (
    PasswordResetTokenRepository,
    RefreshTokenRepository,
    UserRepository,
)
from services.api.src.auth.security import decode_jwt_token
from services.api.src.auth.service import AuthService

# Setup standard bearer token schema extractor
bearer_scheme = HTTPBearer(auto_error=False)


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    """Inject UserRepository context."""
    return UserRepository(session)


def get_token_repository(session: AsyncSession = Depends(get_db)) -> RefreshTokenRepository:
    """Inject RefreshTokenRepository context."""
    return RefreshTokenRepository(session)


def get_reset_token_repository(session: AsyncSession = Depends(get_db)) -> PasswordResetTokenRepository:
    """Inject PasswordResetTokenRepository context."""
    return PasswordResetTokenRepository(session)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    token_repo: RefreshTokenRepository = Depends(get_token_repository),
    reset_token_repo: PasswordResetTokenRepository = Depends(get_reset_token_repository),
) -> AuthService:
    """Inject AuthService context."""
    return AuthService(user_repo, token_repo, reset_token_repo=reset_token_repo)



def get_access_token(
    request: Request,
    bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Extract JWT access token from HTTPOnly cookie or HTTP Authorization header."""
    # Try HTTPOnly Cookie first
    token = request.cookies.get("access_token")
    if token:
        return token

    # Try Authorization Header
    if bearer:
        return bearer.credentials

    # No credentials found
    raise InvalidTokenException()


async def get_current_user(
    token: str = Depends(get_access_token),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    """Validate access token signature and return the active User session model."""
    try:
        payload = decode_jwt_token(token)
        if payload.get("type") != "access":
            raise InvalidTokenException()
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise InvalidTokenException()
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()

    user = await user_repo.get_by_id(uuid.UUID(user_id_str))
    if not user:
        raise InvalidTokenException()

    if not user.is_active:
        raise UserInactiveException()

    return user
