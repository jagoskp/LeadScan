import re
from datetime import datetime
from typing import Any
import uuid
from pydantic import BaseModel, EmailStr, Field, field_validator


class OrganizationResponse(BaseModel):
    """Organization workspace details output representation."""
    id: uuid.UUID
    name: str
    slug: str
    description: str | None = None
    settings: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationCreate(BaseModel):
    """Organization creation input schema."""
    name: str = Field(..., min_length=2, max_length=100, description="Workspace display name")
    slug: str = Field(..., min_length=2, max_length=100, description="URL-friendly unique slug identifier")
    description: str | None = Field(None, max_length=512)
    settings: dict[str, Any] | None = Field(None, description="Optional configuration limits/settings")

    @field_validator("slug")
    @classmethod
    def validate_slug_format(cls, v: str) -> str:
        """Enforce URL-friendly slug formatting (only lowercase, digits, and hyphens)."""
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError("Slug must contain only lowercase letters, numbers, or hyphens")
        return v


class OrganizationUpdate(BaseModel):
    """Organization updates request schema."""
    name: str | None = Field(None, min_length=2, max_length=100)
    slug: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=512)
    settings: dict[str, Any] | None = Field(None)

    @field_validator("slug")
    @classmethod
    def validate_slug_format(cls, v: str | None) -> str | None:
        """Enforce URL-friendly slug formatting if provided."""
        if v is None:
            return v
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError("Slug must contain only lowercase letters, numbers, or hyphens")
        return v


class OrganizationMemberResponse(BaseModel):
    """Organization membership detail output representation."""
    id: uuid.UUID
    organization_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    created_at: datetime
    username: str
    email: str

    class Config:
        from_attributes = True


class InviteMemberRequest(BaseModel):
    """Request schema for adding/inviting workspace members."""
    email: EmailStr = Field(..., description="Email of the user to invite")
    role: str = Field("Member", description="Membership role (Admin, Member)")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Limit membership roles to standard values."""
        allowed = {"Admin", "Member"}
        if v not in allowed:
            raise ValueError("Role must be either 'Admin' or 'Member'")
        return v


class ChangeRoleRequest(BaseModel):
    """Request schema for updating member authority roles."""
    role: str = Field(..., description="Target membership role (Admin, Member)")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Restrict roles that can be updated via this endpoint."""
        allowed = {"Admin", "Member"}
        if v not in allowed:
            raise ValueError("Role must be either 'Admin' or 'Member'")
        return v
