import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.documents.models import Document
    from services.api.src.organization.models import Organization


class StorageProvider(Base):
    """Database model for storing storage provider configuration details."""

    __tablename__ = "storage_providers"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    provider_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # LOCAL, AWS_S3, AZURE_BLOB, GCS, MINIO
    bucket_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    region: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    endpoint_url: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    health_status: Mapped[str] = mapped_column(
        String(20),
        default="HEALTHY",
        nullable=False,
    )  # HEALTHY, DEGRADED, UNHEALTHY
    health_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="StorageProvider.organization_id == Organization.id",
    )


class StorageFile(Base):
    """Database model for tracking registered files and storage lifecycle."""

    __tablename__ = "storage_files"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    storage_provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("storage_providers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    storage_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE",
        nullable=False,
        index=True,
    )  # ACTIVE, SOFT_DELETED, CLEANED
    metadata_log: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=lambda: {},
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
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="StorageFile.user_id == User.id",
    )
    organization: Mapped["Organization"] = relationship(
        "Organization",
        primaryjoin="StorageFile.organization_id == Organization.id",
    )
    document: Mapped["Document | None"] = relationship(
        "Document",
        primaryjoin="StorageFile.document_id == Document.id",
    )
    provider: Mapped["StorageProvider"] = relationship(
        "StorageProvider",
        primaryjoin="StorageFile.storage_provider_id == StorageProvider.id",
    )


class StorageQuota(Base):
    """Database model for managing organization storage limits and current usage."""

    __tablename__ = "storage_quotas"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    max_bytes: Mapped[int] = mapped_column(
        BigInteger,
        default=53687091200,  # Default 50 GB
        nullable=False,
    )
    used_bytes: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )
    file_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
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
    organization: Mapped["Organization"] = relationship(
        "Organization",
        primaryjoin="StorageQuota.organization_id == Organization.id",
    )
