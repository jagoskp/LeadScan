import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ReportFilters(BaseModel):
    """Report query filtering configuration validations."""

    date_start: datetime | None = Field(
        default=None, description="Start date of report period"
    )
    date_end: datetime | None = Field(
        default=None, description="End date of report period"
    )
    file_type: str | None = Field(
        default=None, description="Filter documents by file extension"
    )
    ocr_status: str | None = Field(
        default=None, description="Filter documents by OCR status"
    )
    ai_status: str | None = Field(
        default=None, description="Filter documents by AI status"
    )


class ReportJobCreate(BaseModel):
    """Report generation job trigger request validation schema."""

    name: str = Field(..., min_length=1, max_length=255)
    report_type: str = Field(
        ..., description="Type of report (e.g., ACCURACY_SUMMARY, VOLUME_REPORT)"
    )
    filters: ReportFilters = Field(
        default_factory=lambda: ReportFilters(),
        description="Filter parameters configuration",
    )
    export_format: str = Field(
        ..., description="Target file export format (PDF, CSV, or EXCEL)"
    )

    @field_validator("report_type")
    @classmethod
    def validate_report_type(cls, v: str) -> str:
        """Validate and normalize report type choice."""
        cleaned = v.strip().upper()
        allowed = {"ACCURACY_SUMMARY", "VOLUME_REPORT"}
        if cleaned not in allowed:
            raise ValueError(f"report_type must be one of {sorted(allowed)}")
        return cleaned

    @field_validator("export_format")
    @classmethod
    def validate_export_format(cls, v: str) -> str:
        """Validate and normalize export file format."""
        cleaned = v.strip().upper()
        allowed = {"PDF", "CSV", "EXCEL"}
        if cleaned not in allowed:
            raise ValueError("export_format must be PDF, CSV, or EXCEL")
        return cleaned


class ReportJobResponse(BaseModel):
    """Report generation job details representation."""

    id: uuid.UUID
    report_id: uuid.UUID | None = None
    name: str
    report_type: str
    organization_id: uuid.UUID
    owner_id: uuid.UUID
    filters: dict[str, Any] | None = None
    export_format: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportUpdate(BaseModel):
    """Pacth request for updating report properties."""

    name: str | None = Field(None, min_length=1, max_length=255)
    is_archived: bool | None = Field(None, description="Toggle archived status")


class ReportResponse(BaseModel):
    """Report details and analytics metadata output representation."""

    id: uuid.UUID
    name: str
    report_type: str
    organization_id: uuid.UUID
    owner_id: uuid.UUID
    filters: dict[str, Any] | None = None
    analytics_summary: dict[str, Any] | None = None
    export_format: str
    export_metadata: dict[str, Any] | None = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportHistoryResponse(BaseModel):
    """Audited report history event representation."""

    id: uuid.UUID
    report_id: uuid.UUID | None = None
    report_job_id: uuid.UUID | None = None
    organization_id: uuid.UUID
    user_id: uuid.UUID
    action: str
    details: dict[str, Any] | None = None
    created_at: datetime

    class Config:
        from_attributes = True
