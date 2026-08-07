import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class Company(Base):
    """Database model for Company associated with Leads."""

    __tablename__ = "lead_companies"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    logo_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    industry: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )
    gst_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    departments: Mapped[dict | None] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    employees_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
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
    leads: Mapped[list["Lead"]] = relationship(
        "Lead",
        back_populates="company",
    )


class Lead(Base):
    """Aggregate Root model for Enterprise Lead Record."""

    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    company_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lead_companies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Untitled Lead",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="New",
        nullable=False,
        index=True,
    )
    priority: Mapped[str] = mapped_column(
        String(50),
        default="Medium",
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        String(100),
        default="Camera Scan",
        nullable=False,
    )
    lead_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    is_favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
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
    company: Mapped["Company | None"] = relationship(
        "Company",
        back_populates="leads",
    )
    contacts: Mapped[list["Contact"]] = relationship(
        "Contact",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    timeline_records: Mapped[list["LeadTimeline"]] = relationship(
        "LeadTimeline",
        back_populates="lead",
        cascade="all, delete-orphan",
        order_by="LeadTimeline.created_at.desc()",
    )
    tags: Mapped[list["LeadTag"]] = relationship(
        "LeadTag",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    notes: Mapped[list["LeadNote"]] = relationship(
        "LeadNote",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    attachments: Mapped[list["LeadAttachment"]] = relationship(
        "LeadAttachment",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    history_records: Mapped[list["LeadHistory"]] = relationship(
        "LeadHistory",
        back_populates="lead",
        cascade="all, delete-orphan",
    )
    lead_metadata: Mapped["LeadMetadata | None"] = relationship(
        "LeadMetadata",
        back_populates="lead",
        cascade="all, delete-orphan",
        uselist=False,
    )


class Contact(Base):
    """Database model for Contact associated with a Lead."""

    __tablename__ = "lead_contacts"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    designation: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    phones: Mapped[dict] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    emails: Mapped[dict] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    websites: Mapped[dict] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    addresses: Mapped[dict] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    social_profiles: Mapped[dict] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    custom_fields: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
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
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="contacts",
    )


class LeadStatus(Base):
    """Database model for customizable Lead Status configurations."""

    __tablename__ = "lead_statuses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    color: Mapped[str] = mapped_column(
        String(30),
        default="#3B82F6",
        nullable=False,
    )
    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )


class LeadTimeline(Base):
    """Database model for immutable Lead Timeline event logging."""

    __tablename__ = "lead_timelines"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    metadata_snapshot: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="timeline_records",
    )


class LeadTag(Base):
    """Database model for Lead Tags."""

    __tablename__ = "lead_tags"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tag_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    color: Mapped[str] = mapped_column(
        String(30),
        default="#10B981",
        nullable=False,
    )
    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="tags",
    )


class LeadNote(Base):
    """Database model for Lead Notes."""

    __tablename__ = "lead_notes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_pinned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_internal: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    author_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="notes",
    )


class LeadAttachment(Base):
    """Database model for Lead file attachments."""

    __tablename__ = "lead_attachments"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    file_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    file_type: Mapped[str] = mapped_column(
        String(50),
        default="image/jpeg",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="attachments",
    )


class LeadHistory(Base):
    """Database model storing historical audit snapshots of field edits."""

    __tablename__ = "lead_histories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    change_summary: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    old_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    new_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="history_records",
    )


class LeadMetadata(Base):
    """Database model preserving raw source lineage (OCR, AI, DOM, Review, Sync)."""

    __tablename__ = "lead_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    original_image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    ocr_raw_output: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    ai_understanding_output: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    dom_entity_snapshot: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    review_session_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True,
    )
    google_sync_job_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="lead_metadata",
    )
