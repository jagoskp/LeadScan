import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base


class Asset(Base):
    """Asset core aggregate model representing a digital asset in DAM engine."""

    __tablename__ = "assets"

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
    review_session_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("review_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ocr_result_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ocr_results.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    asset_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="original_scan",
        index=True,
    )  # original_scan, company_logo, thumbnail, preview_image, ocr_overlay, attachment
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="image/jpeg",
    )
    is_immutable: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
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
    versions: Mapped[list["AssetVersion"]] = relationship(
        "AssetVersion", back_populates="asset", cascade="all, delete-orphan"
    )
    asset_metadata: Mapped["AssetMetadata | None"] = relationship(
        "AssetMetadata", back_populates="asset", uselist=False, cascade="all, delete-orphan"
    )
    integrity_record: Mapped["AssetIntegrity | None"] = relationship(
        "AssetIntegrity", back_populates="asset", uselist=False, cascade="all, delete-orphan"
    )
    thumbnails: Mapped[list["AssetThumbnail"]] = relationship(
        "AssetThumbnail", back_populates="asset", cascade="all, delete-orphan"
    )
    audits: Mapped[list["AssetAudit"]] = relationship(
        "AssetAudit", back_populates="asset", cascade="all, delete-orphan"
    )


class AssetVersion(Base):
    """AssetVersion model tracking version history and rollbacks."""

    __tablename__ = "asset_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    checksum_sha256: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="versions")


class AssetMetadata(Base):
    """AssetMetadata model storing EXIF, resolution, DPI, color space, and file size."""

    __tablename__ = "asset_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_size_bytes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    dpi: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    color_space: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default="RGB",
    )
    hash_sha256: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    checksum_md5: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="asset_metadata")


class AssetIntegrity(Base):
    """AssetIntegrity model monitoring checksum verification and corrupt file status."""

    __tablename__ = "asset_integrities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    expected_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    actual_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )
    integrity_status: Mapped[str] = mapped_column(
        String(50),
        default="healthy",
        nullable=False,
    )  # healthy, corrupted, missing, recovered
    last_checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="integrity_record")


class AssetAudit(Base):
    """AssetAudit model logging immutable access & operation audit trails."""

    __tablename__ = "asset_audits"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # upload, download, preview, version_rollback, integrity_check
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    details: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="audits")


class AssetThumbnail(Base):
    """AssetThumbnail model tracking derivative web previews and thumbnails."""

    __tablename__ = "asset_thumbnails"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    thumbnail_type: Mapped[str] = mapped_column(
        String(50),
        default="small",
        nullable=False,
    )  # small, medium, web_preview
    width: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    height: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    asset: Mapped["Asset"] = relationship("Asset", back_populates="thumbnails")


class CompanyLogo(Base):
    """CompanyLogo model for managing company custom logos and default logo fallbacks."""

    __tablename__ = "company_logos"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lead_companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("assets.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    logo_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
