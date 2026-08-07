import uuid
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Contact Schemas
class ContactCreateSchema(BaseModel):
    first_name: str
    last_name: str | None = None
    designation: str | None = None
    is_primary: bool = True
    phones: list[str] = []
    emails: list[str] = []
    websites: list[str] = []
    addresses: list[str] = []
    social_profiles: list[str] = []
    custom_fields: dict[str, Any] = {}


class ContactSchema(ContactCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Company Schemas
class CompanyCreateSchema(BaseModel):
    company_name: str
    logo_url: str | None = None
    industry: str | None = None
    gst_number: str | None = None
    website: str | None = None
    address: str | None = None
    departments: list[str] = []
    employees_count: int | None = None
    notes: str | None = None


class CompanySchema(CompanyCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    departments: list[str] = []
    created_at: datetime
    updated_at: datetime


# Timeline & Tag Schemas
class LeadTimelineSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID
    event_type: str
    title: str
    description: str | None = None
    actor_id: uuid.UUID | None = None
    metadata_snapshot: dict[str, Any] | None = None
    created_at: datetime


class LeadTagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tag_name: str
    color: str = "#10B981"
    is_system: bool = False


class LeadNoteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content: str
    is_pinned: bool = False
    is_internal: bool = True
    author_id: uuid.UUID | None = None
    created_at: datetime


class LeadMetadataSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    original_image_url: str | None = None
    ocr_raw_output: dict[str, Any] | None = None
    ai_understanding_output: dict[str, Any] | None = None
    dom_entity_snapshot: dict[str, Any] | None = None
    review_session_id: uuid.UUID | None = None
    google_sync_job_id: uuid.UUID | None = None


# Core Lead Schemas
class LeadCreateSchema(BaseModel):
    title: str = "Untitled Lead"
    status: str = "New"
    priority: str = "Medium"
    source: str = "Camera Scan"
    lead_score: float = 0.0
    company: CompanyCreateSchema | None = None
    contacts: list[ContactCreateSchema] = []
    tags: list[str] = []
    notes: list[str] = []
    original_image_url: str | None = None
    ocr_raw_output: dict[str, Any] | None = None
    ai_understanding_output: dict[str, Any] | None = None
    dom_entity_snapshot: dict[str, Any] | None = None
    review_session_id: uuid.UUID | None = None
    google_sync_job_id: uuid.UUID | None = None


class LeadUpdateSchema(BaseModel):
    title: str | None = None
    status: str | None = None
    priority: str | None = None
    lead_score: float | None = None
    is_favorite: bool | None = None


class LeadMergeRequestSchema(BaseModel):
    primary_lead_id: uuid.UUID
    secondary_lead_ids: list[uuid.UUID]


class LeadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None
    owner_id: uuid.UUID | None = None
    title: str
    status: str
    priority: str
    source: str
    lead_score: float
    is_favorite: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    company: CompanySchema | None = None
    contacts: list[ContactSchema] = []
    tags: list[LeadTagSchema] = []
    notes: list[LeadNoteSchema] = []
    lead_metadata: LeadMetadataSchema | None = None
