import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.review_workspace.enums import (
    ConfidenceLevel,
    ReviewApprovalStatus,
    ValidationIssueType,
)


class CorrectionHistoryResponse(BaseModel):
    id: uuid.UUID
    item_id: uuid.UUID
    reviewer_id: uuid.UUID | None
    old_value: str | None
    new_value: str | None
    reason: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewItemUpdate(BaseModel):
    current_value: str = Field(..., min_length=1)
    reason: str | None = Field(None, max_length=255)


class ReviewItemResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    field_name: str
    original_value: str | None
    current_value: str | None
    confidence_score: float | None
    confidence_level: ConfidenceLevel
    bounding_box: dict[str, Any] | None
    is_extra_info: bool
    status: ReviewApprovalStatus
    corrections: list[CorrectionHistoryResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class ValidationIssueResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    field_name: str
    issue_type: ValidationIssueType
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewMetadataResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    key: str
    value: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewSessionCreate(BaseModel):
    document_id: uuid.UUID


class ReviewSessionResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    status: ReviewApprovalStatus
    reviewer_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
    items: list[ReviewItemResponse] = Field(default_factory=list)
    validation_issues: list[ValidationIssueResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
