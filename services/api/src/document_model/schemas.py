import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from services.api.src.document_model.enums import (
    DOMDocumentType,
    DOMEntitySource,
    DOMEntityType,
    DOMRelationshipType,
    DOMReviewStatus,
    DOMSectionType,
)


class DocumentMetadataCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(...)


class DocumentMetadataResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    key: str
    value: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentCreate(BaseModel):
    document_type: DOMDocumentType
    organization_id: uuid.UUID | None = None


class DocumentUpdate(BaseModel):
    status: DOMReviewStatus


class EntityAttributeCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(...)
    language: str | None = None
    page: int | None = None
    position: int | None = None


class EntityAttributeUpdate(BaseModel):
    value: str | None = None
    review_status: DOMReviewStatus | None = None


class EntityAttributeResponse(BaseModel):
    id: uuid.UUID
    entity_id: uuid.UUID
    key: str
    value: str
    language: str | None
    page: int | None
    position: int | None
    review_status: DOMReviewStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EntityResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    section_id: uuid.UUID | None
    entity_group_id: uuid.UUID | None
    entity_type: DOMEntityType
    value: str
    normalized_value: str | None
    confidence: float | None
    source: DOMEntitySource
    bounding_box: dict[str, Any] | None
    attributes: list[EntityAttributeResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class EntityGroupResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    group_name: str
    group_type: str | None
    entities: list[EntityResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentSectionResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    section_type: DOMSectionType
    section_index: int
    entities: list[EntityResponse] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class EntityRelationshipResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    source_entity_id: uuid.UUID
    target_entity_id: uuid.UUID
    relationship_type: DOMRelationshipType
    created_at: datetime

    class Config:
        from_attributes = True


class ExtraInformationResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    raw_text: str
    bounding_box: dict[str, Any] | None
    confidence: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class UnknownEntityResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    raw_text: str
    reason: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    organization_id: uuid.UUID | None
    document_type: DOMDocumentType
    status: DOMReviewStatus
    sections: list[DocumentSectionResponse] = Field(default_factory=list)
    entity_groups: list[EntityGroupResponse] = Field(default_factory=list)
    extra_informations: list[ExtraInformationResponse] = Field(
        default_factory=list
    )
    unknown_entities: list[UnknownEntityResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
