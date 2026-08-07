import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class IdentityScoreSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    duplicate_match_id: uuid.UUID
    identity_score: float
    duplicate_score: float
    similarity_score: float
    confidence_score: float


class DuplicateMatchSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    primary_lead_id: uuid.UUID
    secondary_lead_id: uuid.UUID
    duplicate_score: float
    confidence_score: float
    match_type: str
    confidence_level: str
    status: str
    created_at: datetime


class MergeConflictSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    field_name: str
    primary_value: str | None = None
    secondary_value: str | None = None
    resolved_value: str | None = None
    resolution_policy: str


class MergePreviewResponse(BaseModel):
    primary_lead_id: uuid.UUID
    secondary_lead_id: uuid.UUID
    primary_title: str
    secondary_title: str
    conflicts: list[MergeConflictSchema]
    has_conflicts: bool
    duplicate_score: float
    confidence_level: str


class MergeExecuteRequest(BaseModel):
    primary_lead_id: uuid.UUID
    secondary_lead_ids: list[uuid.UUID]
    resolution_policy: str = "keep_original"  # keep_original, keep_latest, keep_highest_confidence, manual
    custom_field_resolutions: dict[str, str] = {}
    reason: str = "Identity Resolution Duplicate Merge"


class MergeHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    primary_lead_id: uuid.UUID
    secondary_lead_id: uuid.UUID
    actor_id: uuid.UUID | None = None
    merge_reason: str | None = None
    duplicate_score: float
    merged_at: datetime
    conflicts: list[MergeConflictSchema] = []


class RollbackHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    merge_history_id: uuid.UUID
    is_restored: bool
    restored_at: datetime | None = None
