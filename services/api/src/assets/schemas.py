import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class AssetMetadataSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    file_size_bytes: int
    width: int | None = None
    height: int | None = None
    dpi: str | None = None
    color_space: str | None = None
    hash_sha256: str
    checksum_md5: str | None = None


class AssetIntegritySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    expected_hash: str
    actual_hash: str | None = None
    integrity_status: str
    last_checked_at: datetime


class AssetVersionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    asset_id: uuid.UUID
    version_number: int
    storage_path: str
    checksum_sha256: str
    created_at: datetime


class AssetThumbnailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    thumbnail_type: str
    width: int
    height: int
    storage_path: str


class AssetAuditSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    action_type: str
    actor_id: uuid.UUID | None = None
    details: dict[str, Any] | None = None
    created_at: datetime


class AssetCreateSchema(BaseModel):
    asset_type: str = "original_scan"
    file_name: str
    mime_type: str = "image/jpeg"
    is_immutable: bool = False
    lead_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None
    review_session_id: uuid.UUID | None = None
    ocr_result_id: uuid.UUID | None = None


class AssetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None
    review_session_id: uuid.UUID | None = None
    ocr_result_id: uuid.UUID | None = None
    owner_id: uuid.UUID | None = None
    asset_type: str
    file_name: str
    storage_path: str
    mime_type: str
    is_immutable: bool
    created_at: datetime
    updated_at: datetime
    asset_metadata: AssetMetadataSchema | None = None
    integrity_record: AssetIntegritySchema | None = None
    versions: list[AssetVersionSchema] = []
    thumbnails: list[AssetThumbnailSchema] = []


class CompanyLogoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    asset_id: uuid.UUID | None = None
    is_default: bool
    logo_url: str
    created_at: datetime
