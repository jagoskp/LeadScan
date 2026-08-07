import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class OrganizationCreateSchema(BaseModel):
    name: str
    logo_url: str | None = None
    timezone: str = "UTC"


class OrganizationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    logo_url: str | None = None
    timezone: str
    status: str
    created_at: datetime


class WorkspaceCreateSchema(BaseModel):
    organization_id: uuid.UUID
    name: str
    is_default: bool = False


class WorkspaceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    is_default: bool
    created_at: datetime


class TeamCreateSchema(BaseModel):
    workspace_id: uuid.UUID
    name: str
    team_lead_id: uuid.UUID | None = None


class TeamSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    name: str
    team_lead_id: uuid.UUID | None = None


class InvitationCreateSchema(BaseModel):
    organization_id: uuid.UUID
    email: str
    role_name: str = "Viewer"


class InvitationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    email: str
    role_name: str
    token: str
    status: str
    expires_at: datetime
    created_at: datetime


class SessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    device_info: str
    ip_address: str
    is_active: bool
    last_active_at: datetime


class AuditLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None
    action: str
    details: dict[str, Any] | None = None
    created_at: datetime
