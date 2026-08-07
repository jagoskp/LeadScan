import uuid
from typing import Any

from pydantic import BaseModel, Field


class RuleConditionSchema(BaseModel):
    logical_operator: str = Field("AND", description="AND / OR / NOT / IF / ELSE")
    criteria: list[dict[str, Any]] = Field(default_factory=list)


class PreviewRequest(BaseModel):
    document_id: uuid.UUID
    profile_id: uuid.UUID


class PreviewResponse(BaseModel):
    document_id: uuid.UUID
    profile_id: uuid.UUID
    original_dom_elements_count: int
    mapped_results: list[dict[str, Any]]
    unmapped_fields: list[dict[str, Any]]
    validation_errors: list[str]
    transformation_applied: list[dict[str, Any]]


class ProfileImportRequest(BaseModel):
    profile_json: dict[str, Any] = Field(
        ..., description="JSON representation of profile"
    )
    organization_id: uuid.UUID | None = None


class ProfileExportResponse(BaseModel):
    profile_id: uuid.UUID
    exported_json: dict[str, Any]
