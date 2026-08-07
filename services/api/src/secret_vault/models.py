import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User


class Secret(Base):
    """Core vault entity tracking secret identity, type, and lifecycle status."""

    __tablename__ = "secrets"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    secret_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="Active"
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    versions: Mapped[list["SecretVersion"]] = relationship(
        "SecretVersion",
        back_populates="secret",
        cascade="all, delete-orphan",
        order_by="SecretVersion.version_number",
    )
    audit_logs: Mapped[list["SecretAudit"]] = relationship(
        "SecretAudit",
        back_populates="secret",
        cascade="all, delete-orphan",
    )
    rotations: Mapped[list["SecretRotation"]] = relationship(
        "SecretRotation",
        back_populates="secret",
        cascade="all, delete-orphan",
    )
    access_grants: Mapped[list["SecretAccess"]] = relationship(
        "SecretAccess",
        back_populates="secret",
        cascade="all, delete-orphan",
    )
    policy: Mapped["SecretPolicy | None"] = relationship(
        "SecretPolicy",
        back_populates="secret",
        cascade="all, delete-orphan",
        uselist=False,
    )
    metadata_tags: Mapped[list["SecretMetadata"]] = relationship(
        "SecretMetadata",
        back_populates="secret",
        cascade="all, delete-orphan",
    )

    # Bindings
    owner: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="Secret.owner_id == User.id",
    )


class SecretVersion(Base):
    """Immutable encrypted snapshot of a secret value at a point in time."""

    __tablename__ = "secret_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    secret_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    encrypted_value: Mapped[str] = mapped_column(Text, nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    key_reference: Mapped[str] = mapped_column(
        String(100), nullable=False, default="master-key-v1"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Relationships
    secret: Mapped["Secret"] = relationship(
        "Secret", back_populates="versions"
    )


class SecretAudit(Base):
    """Full audit trail entry: who, when, why, and version references."""

    __tablename__ = "secret_audits"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    secret_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    old_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    new_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    success: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Relationships
    secret: Mapped["Secret"] = relationship(
        "Secret", back_populates="audit_logs"
    )
    actor: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="SecretAudit.actor_id == User.id",
    )


class SecretRotation(Base):
    """Rotation schedule and execution results for a secret."""

    __tablename__ = "secret_rotations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    secret_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    interval_days: Mapped[int] = mapped_column(
        Integer, nullable=False, default=30
    )
    last_rotated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    next_rotation_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    rotation_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    last_error: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    # Relationships
    secret: Mapped["Secret"] = relationship(
        "Secret", back_populates="rotations"
    )


class SecretAccess(Base):
    """Scoped access grant binding role to user, connector, or organisation."""

    __tablename__ = "secret_accesses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    secret_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    grantee_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    connector_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True, index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Relationships
    secret: Mapped["Secret"] = relationship(
        "Secret", back_populates="access_grants"
    )
    grantee: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="SecretAccess.grantee_user_id == User.id",
    )


class SecretPolicy(Base):
    """Rotation intervals, max version retention, and expiry rules."""

    __tablename__ = "secret_policies"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    secret_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    rotation_interval_days: Mapped[int] = mapped_column(
        Integer, nullable=False, default=90
    )
    max_versions: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10
    )
    auto_rotate: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    expiry_days: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    secret: Mapped["Secret"] = relationship(
        "Secret", back_populates="policy"
    )


class SecretMetadata(Base):
    """Encrypted key-value metadata tags attached to a secret."""

    __tablename__ = "secret_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    secret_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    encrypted_value: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Relationships
    secret: Mapped["Secret"] = relationship(
        "Secret", back_populates="metadata_tags"
    )
