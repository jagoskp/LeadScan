import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class CameraDevice(Base):
    """Database model for registered camera capture devices."""

    __tablename__ = "camera_devices"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    connection_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="CONNECTED",
        nullable=False,
    )
    supported_resolutions: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    supported_framerates: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class CaptureSession(Base):
    """Database model for tracking active camera capture sessions."""

    __tablename__ = "capture_sessions"

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
    device_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("camera_devices.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    resolution: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    framerate: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    format: Mapped[str] = mapped_column(
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    frames: Mapped[list["CapturedFrame"]] = relationship(
        "CapturedFrame",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    # Direct relation bindings (no back-populates to preserve separation)
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="CaptureSession.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="CaptureSession.organization_id == Organization.id",
    )
    device: Mapped["CameraDevice | None"] = relationship(
        "CameraDevice",
        primaryjoin="CaptureSession.device_id == CameraDevice.id",
    )


class CapturedFrame(Base):
    """Database model for storing captured image frame session details."""

    __tablename__ = "captured_frames"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("capture_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
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
    quality_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    quality_checks: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    session: Mapped["CaptureSession"] = relationship(
        "CaptureSession",
        back_populates="frames",
    )
