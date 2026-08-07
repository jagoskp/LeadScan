import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.sync_engine.enums import (
    ConnectorType,
    SyncJobStatus,
    SyncMode,
)


class ConnectorCredentialCreate(BaseModel):
    credential_type: str = Field(..., min_length=1, max_length=50)
    encrypted_token: str
    refresh_token: str | None = None
    expires_at: datetime | None = None


class ConnectorCredentialResponse(BaseModel):
    id: uuid.UUID
    profile_id: uuid.UUID
    credential_type: str
    encrypted_token: str
    refresh_token: str | None
    expires_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorMetadataCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str | None = Field(None, max_length=255)


class ConnectorMetadataResponse(BaseModel):
    id: uuid.UUID
    profile_id: uuid.UUID
    key: str
    value: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorProfileCreate(BaseModel):
    connector_id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=100)
    sync_mode: SyncMode
    organization_id: uuid.UUID | None = None
    credentials: list[ConnectorCredentialCreate] = Field(default_factory=list)
    metadata_records: list[ConnectorMetadataCreate] = Field(default_factory=list)


class ConnectorProfileResponse(BaseModel):
    id: uuid.UUID
    connector_id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    name: str
    sync_mode: SyncMode
    credentials: list[ConnectorCredentialResponse] = Field(default_factory=list)
    metadata_records: list[ConnectorMetadataResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    connector_type: ConnectorType


class ConnectorResponse(BaseModel):
    id: uuid.UUID
    name: str
    connector_type: ConnectorType
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SyncJobCreate(BaseModel):
    profile_id: uuid.UUID
    session_id: uuid.UUID


class SyncHistoryResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    status: SyncJobStatus
    retries_attempted: int
    duration_ms: int | None
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


class SyncJobResponse(BaseModel):
    id: uuid.UUID
    profile_id: uuid.UUID
    session_id: uuid.UUID
    status: SyncJobStatus
    retry_count: int
    max_retries: int
    scheduled_at: datetime | None
    created_at: datetime
    history_logs: list[SyncHistoryResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class SyncResultResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    payload_snapshot: dict[str, Any]
    response_snapshot: dict[str, Any] | None
    created_at: datetime

    class Config:
        from_attributes = True
