import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.ai.models import AIJob
    from services.api.src.auth.models import User
    from services.api.src.documents.models import Document
    from services.api.src.ocr.models import OCRJob
    from services.api.src.organization.models import Organization


class Workflow(Base):
    """Workflow model defining automation workflows and templates."""

    __tablename__ = "workflows"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    trigger_type: Mapped[str] = mapped_column(
        String(50),
        default="lead_created",
        nullable=False,
    )  # lead_created, lead_updated, status_changed, google_sync_completed, duplicate_merged, scheduled
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
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

    rules: Mapped[list["WorkflowRule"]] = relationship(
        "WorkflowRule", back_populates="workflow", cascade="all, delete-orphan"
    )


class WorkflowRule(Base):
    """WorkflowRule model defining IF/THEN conditions for automated actions."""

    __tablename__ = "workflow_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    condition_field: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )  # status, priority, lead_score, tag
    operator: Mapped[str] = mapped_column(
        String(20),
        default="EQUALS",
        nullable=False,
    )  # EQUALS, NOT_EQUALS, CONTAINS, GREATER_THAN
    condition_value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    action_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # create_task, assign_user, change_status, send_notification

    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="rules")


class Task(Base):
    """Task model managing follow-up tasks, assignments, priorities, and statuses."""

    __tablename__ = "workflow_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        default="Medium",
        nullable=False,
    )  # High, Medium, Low
    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
        nullable=False,
    )  # Pending, In Progress, Completed, Cancelled
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
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


class FollowUp(Base):
    """FollowUp model managing communication activities (Call, WhatsApp, Email, Meeting)."""

    __tablename__ = "workflow_followups"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    follow_up_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # phone_call, whatsapp, sms, email, meeting, office_visit, proposal, quotation
    summary: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class Reminder(Base):
    """Reminder model managing one-time and recurring task reminders."""

    __tablename__ = "workflow_reminders"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("workflow_tasks.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    reminder_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    is_triggered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_snoozed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    snooze_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class SLA(Base):
    """SLA model managing response and resolution time targets and breach tracking."""

    __tablename__ = "workflow_slas"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    response_due_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    resolution_due_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    is_response_breached: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_resolution_breached: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class NotificationQueue(Base):
    """NotificationQueue model storing outbound notifications (In-App, Email, SMS, WhatsApp)."""

    __tablename__ = "workflow_notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    channel: Mapped[str] = mapped_column(
        String(50),
        default="in_app",
        nullable=False,
    )  # in_app, email, sms, whatsapp, push
    recipient: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="queued",
        nullable=False,
    )  # queued, sent, failed
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class AutomationLog(Base):
    """AutomationLog model auditing executed workflow automation actions."""

    __tablename__ = "workflow_automation_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
    )
    action_taken: Mapped[str] = mapped_column(
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
