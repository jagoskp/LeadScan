import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class UnderstandingJob(Base):
    """Database model tracking semantic analysis executions."""

    __tablename__ = "understanding_jobs"

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
    ocr_page_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True,
        index=True,
    )
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )
    document_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    detected_language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
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
    entities: Mapped[list["DetectedEntity"]] = relationship(
        "DetectedEntity",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    relations: Mapped[list["EntityRelation"]] = relationship(
        "EntityRelation",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    keywords: Mapped[list["Keyword"]] = relationship(
        "Keyword",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    unknown_entities: Mapped[list["UnknownEntity"]] = relationship(
        "UnknownEntity",
        back_populates="job",
        cascade="all, delete-orphan",
    )

    # Core relationship bindings
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="UnderstandingJob.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="UnderstandingJob.organization_id == Organization.id",
    )


class DetectedEntity(Base):
    """Database model for storing resolved semantic entity values."""

    __tablename__ = "detected_entities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("understanding_jobs.id", ondelete="CASCADE"),
        nullable=False,
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
    job: Mapped["UnderstandingJob"] = relationship(
        "UnderstandingJob",
        back_populates="entities",
    )


class EntityRelation(Base):
    """Database model linking source and target entities together."""

    __tablename__ = "entity_relations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("understanding_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_entity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("detected_entities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_entity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("detected_entities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relation_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
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
    job: Mapped["UnderstandingJob"] = relationship(
        "UnderstandingJob",
        back_populates="relations",
    )
    source_entity: Mapped["DetectedEntity"] = relationship(
        "DetectedEntity",
        foreign_keys=[source_entity_id],
    )
    target_entity: Mapped["DetectedEntity"] = relationship(
        "DetectedEntity",
        foreign_keys=[target_entity_id],
    )


class Keyword(Base):
    """Database model storing key search tokens."""

    __tablename__ = "keywords"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("understanding_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    word: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    job: Mapped["UnderstandingJob"] = relationship(
        "UnderstandingJob",
        back_populates="keywords",
    )


class UnknownEntity(Base):
    """Database model preserving unclassified raw tokens to prevent data loss."""

    __tablename__ = "unknown_entities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("understanding_jobs.id", ondelete="CASCADE"),
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
    job: Mapped["UnderstandingJob"] = relationship(
        "UnderstandingJob",
        back_populates="unknown_entities",
    )


class UnderstandingMetadata(Base):
    """Database model for key-value execution latency statistics."""

    __tablename__ = "understanding_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("understanding_jobs.id", ondelete="CASCADE"),
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

    # Relationship bindings
    job: Mapped["UnderstandingJob"] = relationship(
        "UnderstandingJob",
        primaryjoin="UnderstandingMetadata.job_id == UnderstandingJob.id",
    )
