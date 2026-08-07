import re
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """User account registration input schema."""
    email: EmailStr = Field(..., description="User's unique email address")
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Alphanumeric username (3-30 characters)",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Secure password (minimum 8 characters)",
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Enforce alphanumeric usernames."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username must contain only letters, numbers, underscores, or hyphens"
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

