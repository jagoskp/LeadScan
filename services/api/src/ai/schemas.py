import re
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class AIResultResponse(BaseModel):
    """AI processing analysis output representation."""

    id: uuid.UUID
    job_id: uuid.UUID
    organization_id: uuid.UUID
    document_id: uuid.UUID
    extracted_data: dict[str, Any] | None = None
    raw_response: str | None = None
    tokens_used: int | None = None
    ai_metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIJobResponse(BaseModel):
    """AI job request configuration and status output representation."""

    id: uuid.UUID
    document_id: uuid.UUID
    ocr_result_id: uuid.UUID
    organization_id: uuid.UUID
    owner_id: uuid.UUID
    provider: str
    model_name: str
    prompt_version: str
    status: str
    created_at: datetime
    updated_at: datetime
    result: AIResultResponse | None = None

    class Config:
        from_attributes = True


class AIJobCreate(BaseModel):
    """AI job initialization request input schema."""

    document_id: uuid.UUID = Field(..., description="UUID of document to analyze")
    ocr_result_id: uuid.UUID = Field(
        ..., description="UUID of associated OCR result source"
    )
    provider: str = Field(..., description="AI Provider (OPENAI, GEMINI, or CLAUDE)")
    model_name: str = Field(
        ..., description="Name of LLM model (e.g. gpt-4o, claude-3-5-sonnet)"
    )
    prompt_version: str = Field(
        ..., description="Prompt revision tracking label (e.g., v1.0.0)"
    )

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Validate and normalize AI provider selection."""
        cleaned = v.strip().upper()
        allowed = {"OPENAI", "GEMINI", "CLAUDE"}
        if cleaned not in allowed:
            raise ValueError(
                "AI Provider must be one of 'OPENAI', 'GEMINI', or 'CLAUDE'"
            )
        return cleaned

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Ensure LLM model name parameter is non-empty."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Model name cannot be empty")
        return cleaned

    @field_validator("prompt_version")
    @classmethod
    def validate_prompt_version(cls, v: str) -> str:
        """Validate prompt version string structure."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Prompt version cannot be empty")
        if not re.match(r"^v?[0-9a-zA-Z.-]+$", cleaned):
            raise ValueError(
                "Prompt version must contain only alphanumeric "
                "characters, dots, hyphens, and optional v prefix"
            )
        return cleaned


class AIJobUpdate(BaseModel):
    """AI job manual status transition request schema."""

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
