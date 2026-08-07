import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base


class IdentityProfile(Base):
    """IdentityProfile model storing unified identity attributes across Leads, Companies, and Contacts."""

    __tablename__ = "identity_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    company_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lead_companies.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lead_contacts.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    canonical_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    primary_email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )
    primary_phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    gst_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    pan_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
    )
    domain_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
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


class DuplicateMatch(Base):
    """DuplicateMatch model recording potential duplicate pairs, scores, and confidence classifications."""

    __tablename__ = "duplicate_matches"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    primary_lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    secondary_lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    duplicate_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    match_type: Mapped[str] = mapped_column(
        String(50),
        default="exact",
        nullable=False,
    )  # exact, gst, phone, email, fuzzy, domain
    confidence_level: Mapped[str] = mapped_column(
        String(50),
        default="100%",
        nullable=False,
    )  # 100%, Very High, High, Medium, Low
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )  # pending, merged, ignored, resolved
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class MergeHistory(Base):
    """MergeHistory model logging audit history of lead merge executions."""

    __tablename__ = "merge_histories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    primary_lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    secondary_lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    merge_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    duplicate_score: Mapped[float] = mapped_column(
        Float,
        default=100.0,
        nullable=False,
    )
    merged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    conflicts: Mapped[list["MergeConflict"]] = relationship(
        "MergeConflict", back_populates="merge_history", cascade="all, delete-orphan"
    )
    rollback_record: Mapped["RollbackHistory | None"] = relationship(
        "RollbackHistory", back_populates="merge_history", uselist=False, cascade="all, delete-orphan"
    )


class MergeConflict(Base):
    """MergeConflict model tracking field-level conflicts and resolution policies."""

    __tablename__ = "merge_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    merge_history_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("merge_histories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    primary_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    secondary_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    resolved_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    resolution_policy: Mapped[str] = mapped_column(
        String(50),
        default="keep_original",
        nullable=False,
    )  # keep_original, keep_latest, keep_highest_confidence, manual

    merge_history: Mapped["MergeHistory"] = relationship("MergeHistory", back_populates="conflicts")


class IdentityScore(Base):
    """IdentityScore model storing multi-dimensional similarity and confidence metrics."""

    __tablename__ = "identity_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    duplicate_match_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("duplicate_matches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    identity_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    duplicate_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    similarity_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class RollbackHistory(Base):
    """RollbackHistory model storing pre-merge snapshot data for 100% lossless rollback."""

    __tablename__ = "rollback_histories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    merge_history_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("merge_histories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    snapshot_before_merge: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    is_restored: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    restored_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    merge_history: Mapped["MergeHistory"] = relationship("MergeHistory", back_populates="rollback_record")
