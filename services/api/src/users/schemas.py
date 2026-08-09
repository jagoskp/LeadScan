import re
from datetime import datetime
from typing import Any
import uuid
from pydantic import BaseModel, Field, field_validator


class UserProfileResponse(BaseModel):
    """User profile data serialization response schema."""
    user_id: uuid.UUID
    email: str
    username: str
    full_name: str | None = None
    phone: str | None = None
    company: str | None = None
    designation: str | None = None
    avatar_url: str | None = None
    preferences: dict[str, Any] = Field(default_factory=dict)
    account_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """User profile patch/update request schema."""
    full_name: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, description="Phone number (E.164 or 10-digit format)")
    company: str | None = Field(None, max_length=255)
    designation: str | None = Field(None, max_length=255)
    preferences: dict[str, Any] | None = Field(
        None,
        description="User configuration settings (e.g. notifications, language)",
    )

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, v: str | None) -> str | None:
        """Enforce standard E.164 or 10-digit Indian phone formats if provided."""
        if v is None or not v.strip():
            return v
        cleaned = v.strip()
        if not (re.match(r"^[6-9]\d{9}$", cleaned) or re.match(r"^\+?[1-9]\d{6,14}$", cleaned)):
            raise ValueError("Phone number must match valid 10-digit or international format")
        return cleaned


class ChangePasswordRequest(BaseModel):
    """User request body for changing credentials."""
    current_password: str = Field(..., description="Active user password")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Secure password (minimum 8 characters)",
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
