import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.ocr_engine.enums import (
    OCRInputType,
    OCRJobStatus,
    OCRProviderType,
)


class OCRMetadataCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(...)


class OCRMetadataResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    key: str
    value: str
    created_at: datetime

    class Config:
        from_attributes = True


class OCRJobCreate(BaseModel):
    input_type: OCRInputType
    provider: OCRProviderType
    languages: list[str] = Field(default_factory=lambda: ["en"])
    file_path: str = Field(..., min_length=1, max_length=512)
    organization_id: uuid.UUID | None = None


class OCRJobUpdate(BaseModel):
    status: OCRJobStatus


class OCRWordResponse(BaseModel):
    id: uuid.UUID
    line_id: uuid.UUID
    word_index: int
    text: str
    bounding_box: dict[str, Any] | None
    confidence: float | None
    char_start: int | None
    char_end: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class OCRLineResponse(BaseModel):
    id: uuid.UUID
    block_id: uuid.UUID
    line_index: int
    raw_text: str
    bounding_box: dict[str, Any] | None
    confidence: float | None
    words: list[OCRWordResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class OCRBlockResponse(BaseModel):
    id: uuid.UUID
    page_id: uuid.UUID
    block_index: int
    block_type: str
    bounding_box: dict[str, Any] | None
    confidence: float | None
    lines: list[OCRLineResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class OCRPageResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    page_number: int
    raw_text: str
    width: int | None
    height: int | None
    detected_language: str | None
    confidence_score: float | None
    blocks: list[OCRBlockResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class OCRJobResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    input_type: OCRInputType
    provider: OCRProviderType
    status: OCRJobStatus
    languages: list[str]
    file_path: str
    pages: list[OCRPageResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
