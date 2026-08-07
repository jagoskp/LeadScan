import re
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class OCRResultResponse(BaseModel):
    """OCR processing extraction output representation."""

    id: uuid.UUID
    job_id: uuid.UUID
    organization_id: uuid.UUID
    document_id: uuid.UUID
    raw_text: str | None = None
    confidence: float | None = None
    ocr_metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OCRJobResponse(BaseModel):
    """OCR job request details and status output representation."""

    id: uuid.UUID
    document_id: uuid.UUID
    organization_id: uuid.UUID
    owner_id: uuid.UUID
    engine: str
    language: str
    status: str
    created_at: datetime
    updated_at: datetime
    result: OCRResultResponse | None = None

    class Config:
        from_attributes = True


class OCRJobCreate(BaseModel):
    """OCR job initialization request input schema."""

    document_id: uuid.UUID = Field(..., description="UUID of document to process")
    engine: str = Field("PADDLEOCR", description="OCR engine (PADDLEOCR or TESSERACT)")
    language: str = Field(
        "en", description="BCP 47/ISO 639-1 language code (e.g. en, fr)"
    )

    @field_validator("engine")
    @classmethod
    def validate_engine(cls, v: str) -> str:
        """Validate and normalize OCR engine choice."""
        cleaned = v.strip().upper()
        allowed = {"PADDLEOCR", "TESSERACT"}
        if cleaned not in allowed:
            raise ValueError("OCR Engine must be either 'PADDLEOCR' or 'TESSERACT'")
        return cleaned

    @field_validator("language")
    @classmethod
    def validate_language_code(cls, v: str) -> str:
        """Validate language code structure conforming to ISO 639/BCP 47."""
        cleaned = v.strip().lower()
        if not re.match(r"^[a-z]{2}(-[a-z]{2,4})?$", cleaned):
            raise ValueError(
                "Language must be standard BCP 47/ISO 639-1 code (e.g., 'en', 'zh-cn')"
            )
        return cleaned


class OCRJobUpdate(BaseModel):
    """OCR job manual status transition request schema."""

    status: str = Field(..., description="Target job status to transition to")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Enforce standard status values."""
        cleaned = v.strip().upper()
        allowed = {
            "PENDING",
            "QUEUED",
            "RUNNING",
            "COMPLETED",
            "FAILED",
            "CANCELLED",
        }
        if cleaned not in allowed:
            raise ValueError(f"Status must be one of {sorted(allowed)}")
        return cleaned
