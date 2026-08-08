import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base


class TenantOrganization(Base):
    """TenantOrganization model managing multi-tenant organization accounts."""

    __tablename__ = "tenant_organizations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    logo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    timezone: Mapped[str] = mapped_column(
        String(50),
        default="UTC",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
    )  # active, suspended, archived
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

    workspaces: Mapped[list["Workspace"]] = relationship(
        "Workspace", back_populates="organization", cascade="all, delete-orphan"
    )


class Workspace(Base):
    """Workspace model defining isolated tenant workspace environments."""

    __tablename__ = "tenant_workspaces"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenant_organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
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

    organization: Mapped["TenantOrganization"] = relationship("TenantOrganization", back_populates="workspaces")


class Department(Base):
    """Department model managing organization sub-units."""

    __tablename__ = "tenant_departments"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenant_organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )


class Team(Base):
    """Team model managing cross-functional teams and team leads."""

    __tablename__ = "tenant_teams"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenant_workspaces.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    team_lead_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )


class Role(Base):
    """Role model managing RBAC role definitions (Owner, Admin, Manager, Operator, Reviewer, Viewer)."""

    __tablename__ = "tenant_roles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )  # Owner, Admin, Manager, Operator, Reviewer, Viewer
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )


class Permission(Base):
    """Permission model defining granular capability grants."""

    __tablename__ = "tenant_permissions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenant_roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )  # leads:read, leads:write, leads:delete, google_sync:execute


class Membership(Base):
    """Membership model mapping Users to Organizations, Workspaces, and Roles."""

    __tablename__ = "tenant_memberships"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenant_organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    workspace_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tenant_workspaces.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenant_roles.id", ondelete="RESTRICT"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class Invitation(Base):
    """Invitation model managing tokenized email invitations."""

    __tablename__ = "tenant_invitations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenant_organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )
    role_name: Mapped[str] = mapped_column(
        String(50),
        default="Viewer",
        nullable=False,
    )
    token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
    )  # pending, accepted, rejected, expired
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class Session(Base):
    """Session model managing active user login sessions and device security."""

    __tablename__ = "tenant_user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_info: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    ip_address: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class TenantAuditLog(Base):
    """TenantAuditLog model logging security, permission, and workspace governance events."""

    __tablename__ = "tenant_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tenant_organizations.id", ondelete="CASCADE"),
        nullable=True,
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
    details: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
# Backward-compatible Python alias (not used for SQLAlchemy relationships)
AuditLog = TenantAuditLog
