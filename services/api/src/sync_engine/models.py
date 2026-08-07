import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class Connector(Base):
    """Database model representing registered connectors (e.g. Google Sheets)."""

    __tablename__ = "connectors"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    connector_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    profiles: Mapped[list["ConnectorProfile"]] = relationship(
        "ConnectorProfile",
        back_populates="connector",
        cascade="all, delete-orphan",
    )


class ConnectorProfile(Base):
    """Database model grouping configurations linked to connector targets."""

    __tablename__ = "connector_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    connector_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connectors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    sync_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    connector: Mapped["Connector"] = relationship(
        "Connector",
        back_populates="profiles",
    )
    credentials: Mapped[list["ConnectorCredential"]] = relationship(
        "ConnectorCredential",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    metadata_records: Mapped[list["ConnectorMetadata"]] = relationship(
        "ConnectorMetadata",
        back_populates="profile",
        cascade="all, delete-orphan",
    )

    # Bindings
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="ConnectorProfile.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="ConnectorProfile.organization_id == Organization.id",
    )


class ConnectorCredential(Base):
    """Database model capturing encrypted authentication tokens."""

    __tablename__ = "connector_credentials"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    credential_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    encrypted_token: Mapped[str] = mapped_column(
        nullable=False,
    )
    refresh_token: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    profile: Mapped["ConnectorProfile"] = relationship(
        "ConnectorProfile",
        back_populates="credentials",
    )


class SyncJob(Base):
    """Database model representing jobs in synchronization queues."""

    __tablename__ = "sync_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False,
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    profile: Mapped["ConnectorProfile"] = relationship(
        "ConnectorProfile",
        primaryjoin="SyncJob.profile_id == ConnectorProfile.id",
    )
    history_logs: Mapped[list["SyncHistory"]] = relationship(
        "SyncHistory",
        back_populates="job",
        cascade="all, delete-orphan",
    )


class SyncHistory(Base):
    """Database model logging job status changes, retries, and failure details."""

    __tablename__ = "sync_history"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sync_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    retries_attempted: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    error_message: Mapped[str | None] = mapped_column(
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    job: Mapped["SyncJob"] = relationship(
        "SyncJob",
        back_populates="history_logs",
    )


class SyncResult(Base):
    """Database model caching snapshots of target response outcomes."""

    __tablename__ = "sync_results"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sync_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    payload_snapshot: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    response_snapshot: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class ConnectorMetadata(Base):
    """Database model saving target settings (sheet ID, columns)."""

    __tablename__ = "connector_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_profiles.id", ondelete="CASCADE"),
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

    # Relationships
    profile: Mapped["ConnectorProfile"] = relationship(
        "ConnectorProfile",
        back_populates="metadata_records",
    )
