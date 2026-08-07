import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User


class UserDevice(Base):
    """Database model tracking user registered devices and installation IDs."""

    __tablename__ = "user_devices"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    installation_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    device_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    manufacturer: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    os_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    app_version: Mapped[str] = mapped_column(
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
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", primaryjoin="UserDevice.user_id == User.id")
    sessions: Mapped[list["UserSessionLog"]] = relationship(
        "UserSessionLog",
        back_populates="device",
        cascade="all, delete-orphan",
    )


class UserSubscription(Base):
    """Database model tracking user subscription status and device limits."""

    __tablename__ = "user_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    tier: Mapped[str] = mapped_column(
        String(20),
        default="FREE",  # FREE, PRO, ENTERPRISE
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",  # ACTIVE, EXPIRED, CANCELLED
        nullable=False,
    )
    max_devices: Mapped[int] = mapped_column(
        Integer,
        default=1,  # FREE: 1, PRO: 3, ENTERPRISE: 10
        nullable=False,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", primaryjoin="UserSubscription.user_id == User.id")


class UserSessionLog(Base):
    """Database model for session duration tracking."""

    __tablename__ = "user_session_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    session_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    device: Mapped["UserDevice"] = relationship("UserDevice", back_populates="sessions")


class UserUsageStats(Base):
    """Database table tracking cumulative user feature usage metrics."""

    __tablename__ = "user_usage_stats"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    total_app_opens: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    total_login_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    total_scan_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    total_leads_created: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    total_backup_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    total_sheets_sync_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", primaryjoin="UserUsageStats.user_id == User.id")
