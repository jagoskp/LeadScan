import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class ScanJob(Base):
    """Database model for tracking scan job configurations and status."""

    __tablename__ = "scan_jobs"

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
    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        String(50),
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
    images: Mapped[list["ScanImage"]] = relationship(
        "ScanImage",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    results: Mapped[list["ScanResult"]] = relationship(
        "ScanResult",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    ai_suggestions: Mapped[list["AISuggestion"]] = relationship(
        "AISuggestion",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    metadata_records: Mapped[list["ScanMetadata"]] = relationship(
        "ScanMetadata",
        back_populates="job",
        cascade="all, delete-orphan",
    )

    # Core relationship bindings (no back-populates on user/org to preserve separation)
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="ScanJob.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="ScanJob.organization_id == Organization.id",
    )


class ScanImage(Base):
    """Database model for original scanned image files."""

    __tablename__ = "scan_images"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scan_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    mime_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    file_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    job: Mapped["ScanJob"] = relationship(
        "ScanJob",
        back_populates="images",
    )


class ScanResult(Base):
    """Database model for consolidated scanning pipeline results."""

    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scan_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    logo_url: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )
    logo_status: Mapped[str] = mapped_column(
        String(50),
        default="NONE",
        nullable=False,
    )
    review_status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        nullable=False,
    )
    confidence_score: Mapped[float | None] = mapped_column(
        Float,
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
    job: Mapped["ScanJob"] = relationship(
        "ScanJob",
        back_populates="results",
    )
    detected_fields: Mapped[list["DetectedField"]] = relationship(
        "DetectedField",
        back_populates="result",
        cascade="all, delete-orphan",
    )
    extra_information: Mapped[list["ExtraInformation"]] = relationship(
        "ExtraInformation",
        back_populates="result",
        cascade="all, delete-orphan",
    )


class DetectedField(Base):
    """Database model for a structured metadata attribute.

    Identified in the scan result.
    """

    __tablename__ = "detected_fields"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    result_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scan_results.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    field_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    value: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    bounding_box: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    review_status: Mapped[str] = mapped_column(
        String(50),
        default="UNREVIEWED",
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
    result: Mapped["ScanResult"] = relationship(
        "ScanResult",
        back_populates="detected_fields",
    )


class ExtraInformation(Base):
    """Database model for unmapped raw textual elements identified on the document."""

    __tablename__ = "extra_information"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    result_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scan_results.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    raw_text: Mapped[str] = mapped_column(
        nullable=False,
    )
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    bounding_box: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    result: Mapped["ScanResult"] = relationship(
        "ScanResult",
        back_populates="extra_information",
    )


class AISuggestion(Base):
    """Database model for high-level semantic AI classification and recommendations."""

    __tablename__ = "ai_suggestions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scan_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    suggestion_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    value: Mapped[str] = mapped_column(
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
    job: Mapped["ScanJob"] = relationship(
        "ScanJob",
        back_populates="ai_suggestions",
    )


class ScanMetadata(Base):
    """Database model for generic scanning job metadata properties."""

    __tablename__ = "scan_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scan_jobs.id", ondelete="CASCADE"),
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

    # Relationships
    job: Mapped["ScanJob"] = relationship(
        "ScanJob",
        back_populates="metadata_records",
    )
