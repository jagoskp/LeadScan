import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.ai.models import AIResult
    from services.api.src.auth.models import User
    from services.api.src.documents.models import Document
    from services.api.src.ocr.models import OCRResult
    from services.api.src.organization.models import Organization


class SearchIndex(Base):
    """SearchIndex model mapping indexed text & metadata fields for global search."""

    __tablename__ = "search_indices"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    company_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lead_companies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lead_contacts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ocr_result_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ocr_results.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ai_result_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ai_results.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    content_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    company_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    gst_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )
    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    file_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    ocr_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    ai_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    tags: Mapped[dict | None] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    indexed_fields: Mapped[dict | None] = mapped_column(
        JSON,
        default=dict,
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
    search_metadata_records: Mapped[list["SearchMetadata"]] = relationship(
        "SearchMetadata",
        back_populates="search_index",
        cascade="all, delete-orphan",
    )


class SearchHistory(Base):
    """SearchHistory model logging search queries made by organization users."""

    __tablename__ = "search_histories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    query_string: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    filters: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    results_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class SavedSearch(Base):
    """SavedSearch model for storing bookmarked user searches."""

    __tablename__ = "search_saved"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    query_string: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    filters: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    is_pinned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class SearchFilter(Base):
    """SearchFilter model configuring dynamic global search filter presets."""

    __tablename__ = "search_filters"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    filter_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    filter_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    allowed_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )


class SearchMetadata(Base):
    """SearchMetadata model caching term frequencies and field scoring weights."""

    __tablename__ = "search_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    index_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("search_indices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    term_frequency: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    score_boost: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )
    field_tokens: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    search_index: Mapped["SearchIndex"] = relationship(
        "SearchIndex",
        back_populates="search_metadata_records",
    )
