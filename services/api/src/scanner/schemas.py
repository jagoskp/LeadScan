import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.scanner.enums import (
    AISuggestionType,
    DetectedFieldType,
    FieldReviewStatus,
    LogoStatus,
    ReviewStatus,
    ScanJobStatus,
    ScanSource,
)


class ScanImageCreate(BaseModel):
    file_path: str = Field(..., min_length=1, max_length=512)
    file_name: str = Field(..., min_length=1, max_length=255)
    mime_type: str | None = Field(None, max_length=100)
    file_size: int | None = None
    width: int | None = None
    height: int | None = None


class ScanImageResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    file_path: str
    file_name: str
    mime_type: str | None
    file_size: int | None
    width: int | None
    height: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class ScanJobCreate(BaseModel):
    source: ScanSource
    organization_id: uuid.UUID | None = None
    images: list[ScanImageCreate] = Field(default_factory=list)


class ScanMetadataCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(...)


class ScanMetadataResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    key: str
    value: str
    created_at: datetime

    class Config:
        from_attributes = True


class AISuggestionCreate(BaseModel):
    suggestion_type: AISuggestionType
    value: str
    confidence: float | None = Field(None, ge=0.0, le=1.0)


class AISuggestionResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    suggestion_type: AISuggestionType
    value: str
    confidence: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class ScanJobResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    status: ScanJobStatus
    source: ScanSource
    images: list[ScanImageResponse] = Field(default_factory=list)
    ai_suggestions: list[AISuggestionResponse] = Field(default_factory=list)
    metadata_records: list[ScanMetadataResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DetectedFieldCreate(BaseModel):
    field_name: DetectedFieldType
    field_key: str = Field(..., min_length=1, max_length=100)
    value: str | None = None
    confidence: float | None = Field(None, ge=0.0, le=1.0)
    source: str | None = Field(None, max_length=100)
    bounding_box: dict[str, Any] | None = None
    review_status: FieldReviewStatus = FieldReviewStatus.UNREVIEWED


class DetectedFieldUpdate(BaseModel):
    value: str | None = None
    confidence: float | None = Field(None, ge=0.0, le=1.0)
    review_status: FieldReviewStatus | None = None
    field_key: str | None = Field(None, min_length=1, max_length=100)
    field_name: DetectedFieldType | None = None


class DetectedFieldResponse(BaseModel):
    id: uuid.UUID
    result_id: uuid.UUID
    field_name: str
    field_key: str
    value: str | None
    confidence: float | None
    source: str | None
    bounding_box: dict[str, Any] | None
    review_status: FieldReviewStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExtraInformationCreate(BaseModel):
    raw_text: str
    confidence: float | None = Field(None, ge=0.0, le=1.0)
    bounding_box: dict[str, Any] | None = None


class ExtraInformationResponse(BaseModel):
    id: uuid.UUID
    result_id: uuid.UUID
    raw_text: str
    confidence: float | None
    bounding_box: dict[str, Any] | None
    created_at: datetime

    class Config:
        from_attributes = True


class ScanResultResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    logo_url: str | None
    logo_status: LogoStatus
    review_status: ReviewStatus
    confidence_score: float | None
    detected_fields: list[DetectedFieldResponse] = Field(default_factory=list)
    extra_information: list[ExtraInformationResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Manual Review Payload Schemas
# ----------------------------------------------------

class ManualReviewFieldEdit(BaseModel):
    value: str


class ManualReviewFieldsMerge(BaseModel):
    field_ids: list[uuid.UUID]
    target_field_name: DetectedFieldType
    target_field_key: str
    delimiter: str = " "


class ManualReviewFieldSplit(BaseModel):
    delimiter: str
    new_field_keys: list[str]
    new_field_names: list[DetectedFieldType]


class ManualReviewStatusUpdate(BaseModel):
    review_status: ReviewStatus


# ----------------------------------------------------
# Duplicate Comparison Payload / Response Schemas
# ----------------------------------------------------

class DuplicateComparisonResponse(BaseModel):
    is_duplicate: bool
    potential_duplicate_job_ids: list[uuid.UUID]
    matched_by_fields: list[str]  # e.g., ["Phone", "Email"]
