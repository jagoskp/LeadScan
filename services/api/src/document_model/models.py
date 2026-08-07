import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class Document(Base):
    """Database model representing the DOM Document root node."""

    __tablename__ = "dom_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    sections: Mapped[list["DocumentSection"]] = relationship(
        "DocumentSection",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    entity_groups: Mapped[list["EntityGroup"]] = relationship(
        "EntityGroup",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    extra_informations: Mapped[list["ExtraInformation"]] = relationship(
        "ExtraInformation",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    unknown_entities: Mapped[list["UnknownEntity"]] = relationship(
        "UnknownEntity",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    # Core bindings
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="Document.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="Document.organization_id == Organization.id",
    )


class DocumentSection(Base):
    """Database model for document layout partitions (Header, Body, Footer)."""

    __tablename__ = "dom_sections"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    section_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    section_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="sections",
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity",
        back_populates="section",
        cascade="all, delete-orphan",
    )


class EntityGroup(Base):
    """Database model grouping entities logically (e.g. contact cards)."""

    __tablename__ = "dom_entity_groups"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    group_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    group_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="entity_groups",
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity",
        back_populates="entity_group",
    )


class Entity(Base):
    """Database model representing a single structured DOM Entity node."""

    __tablename__ = "dom_entities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    section_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("dom_sections.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    entity_group_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("dom_entity_groups.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    value: Mapped[str] = mapped_column(
        nullable=False,
    )
    normalized_value: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    section: Mapped["DocumentSection | None"] = relationship(
        "DocumentSection",
        back_populates="entities",
    )
    entity_group: Mapped["EntityGroup | None"] = relationship(
        "EntityGroup",
        back_populates="entities",
    )
    attributes: Mapped[list["EntityAttribute"]] = relationship(
        "EntityAttribute",
        back_populates="entity",
        cascade="all, delete-orphan",
    )


class EntityAttribute(Base):
    """Database model for storing element attributes and positioning."""

    __tablename__ = "dom_entity_attributes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_entities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    value: Mapped[str] = mapped_column(
        nullable=False,
    )
    language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    page: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    position: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    review_status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    entity: Mapped["Entity"] = relationship(
        "Entity",
        back_populates="attributes",
    )


class EntityRelationship(Base):
    """Database model linking two entities (belons_to, parent/child)."""

    __tablename__ = "dom_entity_relationships"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_entity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_entities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_entity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_entities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relationship_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    source_entity: Mapped["Entity"] = relationship(
        "Entity",
        foreign_keys=[source_entity_id],
    )
    target_entity: Mapped["Entity"] = relationship(
        "Entity",
        foreign_keys=[target_entity_id],
    )


class ExtraInformation(Base):
    """Database model preserving unmapped raw text chunks with coordinates."""

    __tablename__ = "dom_extra_informations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    raw_text: Mapped[str] = mapped_column(
        nullable=False,
    )
    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="extra_informations",
    )


class UnknownEntity(Base):
    """Database model preserving unclassified entities."""

    __tablename__ = "dom_unknown_entities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    raw_text: Mapped[str] = mapped_column(
        nullable=False,
    )
    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="unknown_entities",
    )


class DocumentMetadata(Base):
    """Database model for storing job-specific parameters."""

    __tablename__ = "dom_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dom_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    value: Mapped[str] = mapped_column(
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Core relationship bindings
    document: Mapped["Document"] = relationship(
        "Document",
        primaryjoin="DocumentMetadata.document_id == Document.id",
    )
