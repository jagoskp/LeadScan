import re
import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class StorageProviderType(StrEnum):
    LOCAL = "LOCAL"
    AWS_S3 = "AWS_S3"
    AZURE_BLOB = "AZURE_BLOB"
    GCS = "GCS"
    MINIO = "MINIO"


class StorageFileStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SOFT_DELETED = "SOFT_DELETED"
    CLEANED = "CLEANED"


class StorageHealthStatus(StrEnum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"


# ----------------------------------------------------
# Storage Provider Schemas
# ----------------------------------------------------


class StorageProviderCreate(BaseModel):
    organization_id: uuid.UUID | None = None
    name: str = Field(..., min_length=1, max_length=100)
    provider_type: StorageProviderType
    bucket_name: str = Field(..., min_length=3, max_length=255)
    region: str | None = Field(None, max_length=50)
    endpoint_url: str | None = Field(None, max_length=512)
    is_active: bool = True
    is_default: bool = False

    @field_validator("bucket_name")
    @classmethod
    def validate_bucket_name(cls, v: str) -> str:
        """Validate bucket name matching S3/blob standard guidelines."""
        # Lowercase, alphanumeric, dot, dash, underscore
        bucket_regex = r"^[a-z0-9._-]+$"
        if not re.match(bucket_regex, v):
            raise ValueError(
                "Bucket name must contain only lowercase letters, "
                "numbers, periods, hyphens, or underscores"
            )
        return v


class StorageProviderUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    provider_type: StorageProviderType | None = None
    bucket_name: str | None = Field(None, min_length=3, max_length=255)
    region: str | None = Field(None, max_length=50)
    endpoint_url: str | None = Field(None, max_length=512)
    is_active: bool | None = None
    is_default: bool | None = None
    health_status: StorageHealthStatus | None = None


class StorageProviderResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID | None
    name: str
    provider_type: StorageProviderType
    bucket_name: str
    region: str | None
    endpoint_url: str | None
    is_active: bool
    is_default: bool
    health_status: StorageHealthStatus
    health_checked_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Storage File Schemas
# ----------------------------------------------------


class StorageFileCreate(BaseModel):
    document_id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None
    organization_id: uuid.UUID
    storage_provider_id: uuid.UUID
    storage_path: str = Field(..., min_length=1, max_length=512)
    file_size: int = Field(..., ge=0)
    mime_type: str = Field(..., min_length=1, max_length=100)
    original_filename: str = Field(..., min_length=1, max_length=255)
    metadata_log: dict[str, Any] = Field(default_factory=dict)

    @field_validator("storage_path")
    @classmethod
    def validate_storage_path(cls, v: str) -> str:
        """Ensure storage path is non-empty and well-formed."""
        if not v.strip():
            raise ValueError("Storage path cannot be whitespace only")
        return v.strip()


class StorageFileUpdate(BaseModel):
    status: StorageFileStatus | None = None
    metadata_log: dict[str, Any] | None = None


class StorageFileResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID | None
    user_id: uuid.UUID | None
    organization_id: uuid.UUID
    storage_provider_id: uuid.UUID
    storage_path: str
    file_size: int
    mime_type: str
    original_filename: str
    status: StorageFileStatus
    metadata_log: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Storage Quota Schemas
# ----------------------------------------------------


class StorageQuotaUpdate(BaseModel):
    max_bytes: int = Field(..., ge=0)


class StorageQuotaResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    max_bytes: int
    used_bytes: int
    file_count: int
    percentage_used: float = 0.0
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def calculate_percentage(self) -> "StorageQuotaResponse":
        """Compute the quota usage percentage based on bytes limits."""
        if self.max_bytes > 0:
            self.percentage_used = round((self.used_bytes / self.max_bytes) * 100, 2)
        else:
            self.percentage_used = 100.0
        return self

    class Config:
        from_attributes = True
