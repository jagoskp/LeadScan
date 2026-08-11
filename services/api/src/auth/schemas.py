import re
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """User account registration input schema."""
    email: EmailStr = Field(..., description="User's unique email address")
    username: str | None = Field(
        None,
        max_length=255,
        description="Username or email identity (up to 255 characters)",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Secure password (minimum 8 characters)",
    )
    full_name: str | None = Field(None, max_length=255, description="User's full display name")
    phone: str | None = Field(None, max_length=20, description="User's primary phone number")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str | None) -> str | None:
        """Enforce valid username or email identity format."""
        if v is None:
            return v
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v) and not re.match(r"^[a-zA-Z0-9._-]+$", v):
            raise ValueError(
                "Username must be a valid email address or alphanumeric identifier"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Enforce standard enterprise password strength guidelines."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLoginRequest(BaseModel):
    """User account login input schema supporting email or username identifier."""
    identifier: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Email address or username",
    )
    password: str = Field(..., description="User's plain password")


class UserResponse(BaseModel):
    """User account profile output representation."""
    id: uuid.UUID
    email: str
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Authentication tokens response schema."""
    access_token: str = Field(..., description="JWT Access Token")
    token_type: str = Field("bearer", description="Token schema type")
    refresh_token: str = Field(..., description="JWT Refresh Token")


class GoogleLoginRequest(BaseModel):
    """Google OAuth / ID Token authentication request schema."""
    id_token: str = Field(..., description="Google ID Token or credential string")
    email: EmailStr | None = Field(None, description="Extracted user email address from Google payload")
    name: str | None = Field(None, description="User's display name from Google profile")
    photo_url: str | None = Field(None, description="User's Google avatar photo URL")


class ForgotPasswordRequest(BaseModel):
    """Input payload for initiating password reset workflow."""
    email: EmailStr = Field(..., description="User's registered email address")


class ResetPasswordRequest(BaseModel):
    """Input payload for executing password reset with reset token."""
    token: str = Field(..., min_length=1, description="Password reset verification token")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New secure password",
    )

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Enforce standard enterprise password strength guidelines."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


