import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User


class Connector(Base):
    """Database model storing registered connectors
    configurations (e.g. Google Sheets).
    """

    __tablename__ = "connector_studios"

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
    version: Mapped[str] = mapped_column(
        String(20),
        default="1.0.0",
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
    accounts: Mapped[list["ConnectorAccount"]] = relationship(
        "ConnectorAccount",
        back_populates="connector",
        cascade="all, delete-orphan",
    )


class ConnectorAccount(Base):
    """Database model representing integrated external user accounts."""

    __tablename__ = "connector_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    connector_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_studios.id", ondelete="CASCADE"),
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
    account_email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    account_label: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
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
        back_populates="accounts",
    )
    connections: Mapped[list["ConnectorConnection"]] = relationship(
        "ConnectorConnection",
        back_populates="account",
        cascade="all, delete-orphan",
    )


class ConnectorConnection(Base):
    """Database model configuring configured connection links."""

    __tablename__ = "connector_connections"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    labels: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )
    tags: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    account: Mapped["ConnectorAccount"] = relationship(
        "ConnectorAccount",
        back_populates="connections",
    )
    credentials: Mapped[list["ConnectorCredential"]] = relationship(
        "ConnectorCredential",
        back_populates="connection",
        cascade="all, delete-orphan",
    )
    health_records: Mapped[list["ConnectorHealth"]] = relationship(
        "ConnectorHealth",
        back_populates="connection",
        cascade="all, delete-orphan",
    )
    audit_logs: Mapped[list["ConnectorAudit"]] = relationship(
        "ConnectorAudit",
        back_populates="connection",
        cascade="all, delete-orphan",
    )
    permissions: Mapped[list["ConnectorPermission"]] = relationship(
        "ConnectorPermission",
        back_populates="connection",
        cascade="all, delete-orphan",
    )


class ConnectorCredential(Base):
    """Database model holding access credentials keys."""

    __tablename__ = "connector_credentials_studio"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    connection_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_connections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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
    connection: Mapped["ConnectorConnection"] = relationship(
        "ConnectorConnection",
        back_populates="credentials",
    )


class ConnectorHealth(Base):
    """Database model logging latency and connections health checks."""

    __tablename__ = "connector_health"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    connection_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_connections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    last_checked: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    error_message: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    # Relationships
    connection: Mapped["ConnectorConnection"] = relationship(
        "ConnectorConnection",
        back_populates="health_records",
    )


class ConnectorAudit(Base):
    """Database model auditing user logins, rotations, and sync changes."""

    __tablename__ = "connector_audits"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    connection_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_connections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    details: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    connection: Mapped["ConnectorConnection"] = relationship(
        "ConnectorConnection",
        back_populates="audit_logs",
    )

    # Bindings
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="ConnectorAudit.user_id == User.id",
    )


class ConnectorPermission(Base):
    """Database model tracking specific user roles permission configurations."""

    __tablename__ = "connector_permissions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    connection_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("connector_connections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    permission_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    connection: Mapped["ConnectorConnection"] = relationship(
        "ConnectorConnection",
        back_populates="permissions",
    )

    # Bindings
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="ConnectorPermission.user_id == User.id",
    )
