import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User


class ReviewSession(Base):
    """Database model storing user review sessions settings."""

    __tablename__ = "review_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
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
    items: Mapped[list["ReviewItem"]] = relationship(
        "ReviewItem",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    validation_issues: Mapped[list["ValidationIssue"]] = relationship(
        "ValidationIssue",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    # Bindings
    reviewer: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="ReviewSession.reviewer_id == User.id",
    )


class ReviewItem(Base):
    """Database model holding individual data properties awaiting review."""

    __tablename__ = "review_items"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("review_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    original_value: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    current_value: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    confidence_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    is_extra_info: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    session: Mapped["ReviewSession"] = relationship(
        "ReviewSession",
        back_populates="items",
    )
    corrections: Mapped[list["CorrectionHistory"]] = relationship(
        "CorrectionHistory",
        back_populates="item",
        cascade="all, delete-orphan",
    )


class CorrectionHistory(Base):
    """Database model recording edits made to review items."""

    __tablename__ = "correction_history"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("review_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    old_value: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    new_value: Mapped[str | None] = mapped_column(
        nullable=True,
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
    item: Mapped["ReviewItem"] = relationship(
        "ReviewItem",
        back_populates="corrections",
    )

    # Bindings
    reviewer: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="CorrectionHistory.reviewer_id == User.id",
    )


class ValidationIssue(Base):
    """Database model identifying format validation warnings."""

    __tablename__ = "validation_issues"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("review_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    issue_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    session: Mapped["ReviewSession"] = relationship(
        "ReviewSession",
        back_populates="validation_issues",
    )


class ReviewMetadata(Base):
    """Database model storing review session runtime metadata tags."""

    __tablename__ = "review_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("review_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    value: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
