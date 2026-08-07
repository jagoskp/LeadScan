import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


# Search Filters Schema
class UniversalSearchFilterSchema(BaseModel):
    date_from: datetime | None = None
    date_to: datetime | None = None
    status: str | None = None
    owner_id: uuid.UUID | None = None
    tags: list[str] = []
    company_name: str | None = None
    source_type: str | None = None


# Search Query & Execution Schema
class UniversalSearchRequest(BaseModel):
    query: str
    filters: UniversalSearchFilterSchema | None = None
    sort_by: str = "relevance"  # relevance, newest, oldest, alphabetical, score
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class SearchResultItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID | None = None
    document_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None
    title: str
    company_name: str | None = None
    gst_number: str | None = None
    email: str | None = None
    phone: str | None = None
    matched_field: str
    highlighted_match: str
    score: float
    source_type: str
    created_at: datetime


class UniversalSearchResponse(BaseModel):
    query: str
    total_matches: int
    results: list[SearchResultItemSchema]
    page: int
    page_size: int


# Saved & Recent Search Schemas
class SavedSearchCreateSchema(BaseModel):
    title: str
    query_string: str
    filters: dict[str, Any] | None = None
    is_pinned: bool = False


class SavedSearchSchema(SavedSearchCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime


class RecentSearchSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    query_string: str | None = None
    results_count: int
    created_at: datetime


class AutocompleteSuggestionSchema(BaseModel):
    suggestion: str
    target_field: str
    score: float
