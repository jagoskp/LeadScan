import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AuditEventType(StrEnum):
    AUTHENTICATION = "Authentication"
    USER = "User"
    ORGANIZATION = "Organization"
    DOCUMENT = "Document"
    OCR = "OCR"
    AI = "AI"
    WORKFLOW = "Workflow"
    SEARCH = "Search"
    REPORT = "Report"
    NOTIFICATION = "Notification"
    SECURITY = "Security"


class AuditSeverity(StrEnum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"
    CRITICAL = "Critical"


# ----------------------------------------------------
# Audit Log Schemas
# ----------------------------------------------------


class AuditLogCreate(BaseModel):
    user_id: uuid.UUID | None = None
    organization_id: uuid.UUID | None = None
    event_type: AuditEventType
    severity: AuditSeverity = AuditSeverity.INFO
    action: str = Field(..., min_length=1, max_length=100)
    resource_type: str | None = Field(None, max_length=50)
    resource_id: str | None = Field(None, max_length=100)
    document_id: uuid.UUID | None = None
    ocr_job_id: uuid.UUID | None = None
    ai_job_id: uuid.UUID | None = None
    workflow_id: uuid.UUID | None = None
    status: str = Field("SUCCESS", max_length=20)
    ip_address: str | None = Field(None, max_length=45)
    user_agent: str | None = Field(None, max_length=512)
    details: dict[str, Any] = Field(default_factory=dict)


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    event_type: AuditEventType
    severity: AuditSeverity
    action: str
    resource_type: str | None
    resource_id: str | None
    document_id: uuid.UUID | None
    ocr_job_id: uuid.UUID | None
    ai_job_id: uuid.UUID | None
    workflow_id: uuid.UUID | None
    status: str
    ip_address: str | None
    user_agent: str | None
    details: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    page: int
    size: int


# ----------------------------------------------------
# Activity Log Schemas
# ----------------------------------------------------


class ActivityLogCreate(BaseModel):
    user_id: uuid.UUID
    organization_id: uuid.UUID | None = None
    action: str = Field(..., min_length=1, max_length=100)
    resource_type: str = Field(..., min_length=1, max_length=50)
    resource_id: str = Field(..., min_length=1, max_length=100)
    document_id: uuid.UUID | None = None
    ocr_job_id: uuid.UUID | None = None
    ai_job_id: uuid.UUID | None = None
    workflow_id: uuid.UUID | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ActivityLogResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID | None
    action: str
    resource_type: str
    resource_id: str
    document_id: uuid.UUID | None
    ocr_job_id: uuid.UUID | None
    ai_job_id: uuid.UUID | None
    workflow_id: uuid.UUID | None
    details: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityLogListResponse(BaseModel):
    items: list[ActivityLogResponse]
    total: int
    page: int
    size: int


# ----------------------------------------------------
# Security Event Schemas
# ----------------------------------------------------


class SecurityEventCreate(BaseModel):
    user_id: uuid.UUID | None = None
    organization_id: uuid.UUID | None = None
    event_type: str = Field(..., min_length=1, max_length=50)
    severity: AuditSeverity = AuditSeverity.INFO
    ip_address: str = Field(..., min_length=1, max_length=45)
    user_agent: str | None = Field(None, max_length=512)
    metadata_log: dict[str, Any] = Field(default_factory=dict)


class SecurityEventResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    event_type: str
    severity: AuditSeverity
    ip_address: str
    user_agent: str | None
    metadata_log: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class SecurityEventListResponse(BaseModel):
    items: list[SecurityEventResponse]
    total: int
    page: int
    size: int
