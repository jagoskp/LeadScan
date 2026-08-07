import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from services.api.src.connectors.enums import (
    ConnectorHealthStatus,
    ConnectorPermissionType,
)


class ConnectorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    connector_type: str = Field(..., min_length=1, max_length=50)
    version: str = "1.0.0"


class ConnectorResponse(BaseModel):
    id: uuid.UUID
    name: str
    connector_type: str
    version: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorAccountCreate(BaseModel):
    connector_id: uuid.UUID
    account_email: str = Field(..., min_length=1, max_length=150)
    account_label: str | None = Field(None, max_length=100)
    is_default: bool = False
    organization_id: uuid.UUID | None = None


class ConnectorAccountResponse(BaseModel):
    id: uuid.UUID
    connector_id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    account_email: str
    account_label: str | None
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorConnectionCreate(BaseModel):
    account_id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=100)
    labels: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    plain_token: str = Field(..., min_length=1)


class ConnectorConnectionUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    is_enabled: bool | None = None
    labels: list[str] | None = None
    tags: list[str] | None = None


class ConnectorCredentialResponse(BaseModel):
    id: uuid.UUID
    connection_id: uuid.UUID
    encrypted_token: str
    refresh_token: str | None
    expires_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorHealthResponse(BaseModel):
    id: uuid.UUID
    connection_id: uuid.UUID
    status: ConnectorHealthStatus
    last_checked: datetime
    latency_ms: int | None
    error_message: str | None

    class Config:
        from_attributes = True


class ConnectorAuditResponse(BaseModel):
    id: uuid.UUID
    connection_id: uuid.UUID
    user_id: uuid.UUID | None
    action: str
    details: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorPermissionResponse(BaseModel):
    id: uuid.UUID
    connection_id: uuid.UUID
    user_id: uuid.UUID | None
    permission_type: ConnectorPermissionType
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectorConnectionResponse(BaseModel):
    id: uuid.UUID
    account_id: uuid.UUID
    name: str
    is_enabled: bool
    labels: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    credentials: list[ConnectorCredentialResponse] = Field(default_factory=list)
    health_records: list[ConnectorHealthResponse] = Field(default_factory=list)
    audit_logs: list[ConnectorAuditResponse] = Field(default_factory=list)
    permissions: list[ConnectorPermissionResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True
