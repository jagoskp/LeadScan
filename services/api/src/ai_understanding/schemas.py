import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.ai_understanding.enums import (
    AIDocumentType,
    AIJobStatus,
    AIProviderType,
)


class UnderstandingMetadataCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(...)


class UnderstandingMetadataResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    key: str
    value: str
    created_at: datetime

    class Config:
        from_attributes = True


class UnderstandingJobCreate(BaseModel):
    ocr_page_id: uuid.UUID
    provider: AIProviderType
    document_type: AIDocumentType = AIDocumentType.UNKNOWN
    organization_id: uuid.UUID | None = None


class UnderstandingJobUpdate(BaseModel):
    status: AIJobStatus
    document_type: AIDocumentType | None = None


class DetectedEntityResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    entity_type: str
    value: str
    normalized_value: str | None
    bounding_box: dict[str, Any] | None
    confidence: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class EntityRelationResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    source_entity_id: uuid.UUID
    target_entity_id: uuid.UUID
    relation_type: str
    confidence: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class KeywordResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    word: str
    score: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class UnknownEntityResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    raw_text: str
    reason: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class UnderstandingJobResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    ocr_page_id: uuid.UUID | None
    provider: AIProviderType
    status: AIJobStatus
    document_type: AIDocumentType | None
    detected_language: str | None
    entities: list[DetectedEntityResponse] = Field(default_factory=list)
    relations: list[EntityRelationResponse] = Field(default_factory=list)
    keywords: list[KeywordResponse] = Field(default_factory=list)
    unknown_entities: list[UnknownEntityResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
