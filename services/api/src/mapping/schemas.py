import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.mapping.enums import (
    MappingFieldType,
    MappingTargetType,
    TransformationType,
    ValidationRuleType,
)


class TransformationRuleCreate(BaseModel):
    transformation_type: TransformationType
    parameters: dict[str, Any] | None = None
    sequence_order: int = 0


class TransformationRuleResponse(BaseModel):
    id: uuid.UUID
    rule_id: uuid.UUID
    transformation_type: TransformationType
    parameters: dict[str, Any] | None
    sequence_order: int
    created_at: datetime

    class Config:
        from_attributes = True


class ValidationRuleCreate(BaseModel):
    validation_type: ValidationRuleType
    parameters: dict[str, Any] | None = None


class ValidationRuleResponse(BaseModel):
    id: uuid.UUID
    rule_id: uuid.UUID
    validation_type: ValidationRuleType
    parameters: dict[str, Any] | None
    created_at: datetime

    class Config:
        from_attributes = True


class MappingRuleCreate(BaseModel):
    target_field_name: str = Field(..., min_length=1, max_length=100)
    source_entity_type: str = Field(..., min_length=1, max_length=50)
    field_type: MappingFieldType
    is_required: bool = False
    default_value: str | None = None
    transformations: list[TransformationRuleCreate] = Field(default_factory=list)
    validations: list[ValidationRuleCreate] = Field(default_factory=list)


class MappingRuleResponse(BaseModel):
    id: uuid.UUID
    profile_id: uuid.UUID
    target_field_name: str
    source_entity_type: str
    field_type: MappingFieldType
    is_required: bool
    default_value: str | None
    transformations: list[TransformationRuleResponse] = Field(default_factory=list)
    validations: list[ValidationRuleResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class MappingTargetCreate(BaseModel):
    target_type: MappingTargetType
    configuration: dict[str, Any] | None = None


class MappingTargetResponse(BaseModel):
    id: uuid.UUID
    profile_id: uuid.UUID
    target_type: MappingTargetType
    configuration: dict[str, Any] | None
    created_at: datetime

    class Config:
        from_attributes = True


class MappingProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    document_type: str = Field(..., min_length=1, max_length=50)
    organization_id: uuid.UUID | None = None
    rules: list[MappingRuleCreate] = Field(default_factory=list)
    targets: list[MappingTargetCreate] = Field(default_factory=list)


class MappingProfileUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    is_active: bool | None = None


class MappedFieldResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    profile_id: uuid.UUID | None
    rule_id: uuid.UUID | None
    field_name: str
    value: str
    confidence: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class UnmappedFieldResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    profile_id: uuid.UUID | None
    raw_text: str
    bounding_box: dict[str, Any] | None
    created_at: datetime

    class Config:
        from_attributes = True


class MappingHistoryResponse(BaseModel):
    id: uuid.UUID
    profile_id: uuid.UUID
    version: int
    author_id: uuid.UUID | None
    change_summary: str | None
    snapshot: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class MappingProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    name: str
    document_type: str
    version: int
    is_active: bool
    rules: list[MappingRuleResponse] = Field(default_factory=list)
    targets: list[MappingTargetResponse] = Field(default_factory=list)
    history: list[MappingHistoryResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
