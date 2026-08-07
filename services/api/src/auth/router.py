from typing import Any
from fastapi import APIRouter, Depends, Response, Request, status
from leadscan_config import AppSettings
from services.api.src.auth.dependencies import get_auth_service, get_current_user
from services.api.src.auth.exceptions import InvalidTokenException
from services.api.src.auth.models import User
from services.api.src.auth.schemas import (
    GoogleLoginRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from services.api.src.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
settings = AppSettings()

# Helper function to assign secure HTTPOnly cookies
def set_auth_cookies(response: Response, tokens: dict[str, str]) -> None:
    is_secure = settings.APP_ENV == "production"
    
    # Access token cookie
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=is_secure,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    
    # Refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=is_secure,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )


# Helper function to delete auth cookies
def delete_auth_cookies(response: Response) -> None:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: UserRegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """Register a new user account with validated credentials."""
    return await auth_service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """Authenticate user credentials and establish session cookies."""
    user = await auth_service.authenticate(data)
    tokens = await auth_service.create_tokens(user)
    set_auth_cookies(response, tokens)
    return tokens


@router.post("/google", response_model=TokenResponse)
async def google_login(
    data: GoogleLoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """Authenticate user via Google ID Token, creating or restoring user session."""
    tokens = await auth_service.google_authenticate(data)
    set_auth_cookies(response, tokens)
    return tokens



@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """Rotate JWT session tokens using active HTTPOnly refresh token cookie."""
    # Attempt to read refresh token from cookies
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        # Fallback to authorization bearer or JSON body would go here if needed,
        # but for security, HTTPOnly cookie is standard.
        raise InvalidTokenException()

    tokens = await auth_service.refresh_session(refresh_token)
    set_auth_cookies(response, tokens)
    return tokens


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    """Terminate user session by revoking the refresh token and clearing client cookies."""
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await auth_service.logout(refresh_token)
    delete_auth_cookies(response)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> Any:
    """Retrieve profile data for the active logged-in user session."""
    return current_user
