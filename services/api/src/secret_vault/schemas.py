import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from services.api.src.secret_vault.enums import (
    AuditAction,
    SecretAccessRole,
    SecretStatus,
    SecretType,
)

# ── Secret ─────────────────────────────────────────────

class SecretCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    secret_type: SecretType
    plain_value: str = Field(..., min_length=1)
    expires_at: datetime | None = None


class SecretUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    expires_at: datetime | None = None


class SecretResponse(BaseModel):
    id: uuid.UUID
    name: str
    secret_type: SecretType
    status: SecretStatus
    owner_id: uuid.UUID | None
    expires_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── SecretVersion ──────────────────────────────────────

class SecretVersionResponse(BaseModel):
    id: uuid.UUID
    secret_id: uuid.UUID
    version_number: int
    checksum: str
    key_reference: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Rotate ─────────────────────────────────────────────

class SecretRotateRequest(BaseModel):
    new_plain_value: str = Field(..., min_length=1)
    reason: str | None = Field(None, max_length=255)


# ── Access ─────────────────────────────────────────────

class SecretAccessCreate(BaseModel):
    grantee_user_id: uuid.UUID | None = None
    connector_id: uuid.UUID | None = None
    role: SecretAccessRole


class SecretAccessResponse(BaseModel):
    id: uuid.UUID
    secret_id: uuid.UUID
    grantee_user_id: uuid.UUID | None
    connector_id: uuid.UUID | None
    role: SecretAccessRole
    created_at: datetime

    class Config:
        from_attributes = True


# ── Policy ─────────────────────────────────────────────

class SecretPolicyCreate(BaseModel):
    rotation_interval_days: int = Field(90, ge=1)
    max_versions: int = Field(10, ge=1, le=100)
    auto_rotate: bool = False
    expiry_days: int | None = Field(None, ge=1)


class SecretPolicyResponse(BaseModel):
    id: uuid.UUID
    secret_id: uuid.UUID
    rotation_interval_days: int
    max_versions: int
    auto_rotate: bool
    expiry_days: int | None

    class Config:
        from_attributes = True


# ── Audit ──────────────────────────────────────────────

class SecretAuditResponse(BaseModel):
    id: uuid.UUID
    secret_id: uuid.UUID
    actor_id: uuid.UUID | None
    action: AuditAction
    reason: str | None
    old_version: int | None
    new_version: int | None
    success: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Metadata ───────────────────────────────────────────

class SecretMetadataCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    plain_value: str = Field(..., min_length=1)
