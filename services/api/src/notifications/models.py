import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.auth.models import User
    from services.api.src.organization.models import Organization


class NotificationTemplate(Base):
    """Database model for storing notification templates."""
    __tablename__ = "notification_templates"

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
        index=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    notification_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )  # EMAIL, SMS, PUSH, IN_APP, WEBHOOK
    title_template: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    body_template: Mapped[str] = mapped_column(
        String(4000),
        nullable=False,
    )
    variables: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
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
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="NotificationTemplate.organization_id == Organization.id",
    )


class NotificationPreference(Base):
    """Database model for tracking user notification preferences."""
    __tablename__ = "notification_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    notification_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )  # EMAIL, SMS, PUSH, IN_APP, WEBHOOK
    channel_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    preferences: Mapped[dict[str, Any]] = mapped_column(
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

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        primaryjoin="NotificationPreference.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="NotificationPreference.organization_id == Organization.id",
    )


class Notification(Base):
    """Database model for storing and tracking notifications."""
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("notification_templates.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    notification_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )  # EMAIL, SMS, PUSH, IN_APP, WEBHOOK
    recipient: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
        nullable=False,
    )  # LOW, MEDIUM, HIGH, URGENT
    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False,
        index=True,
    )  # PENDING, QUEUED, SENT, DELIVERED, FAILED, READ
    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    body: Mapped[str] = mapped_column(
        String(10000),
        nullable=False,
    )
    queue_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=lambda: {},
        nullable=False,
    )
    status_history: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON,
        default=lambda: [],
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
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        primaryjoin="Notification.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="Notification.organization_id == Organization.id",
    )
    template: Mapped["NotificationTemplate | None"] = relationship(
        "NotificationTemplate",
        primaryjoin="Notification.template_id == NotificationTemplate.id",
    )
