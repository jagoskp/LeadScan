import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base

if TYPE_CHECKING:
    from services.api.src.ai.models import AIJob
    from services.api.src.auth.models import User
    from services.api.src.documents.models import Document
    from services.api.src.ocr.models import OCRJob
    from services.api.src.organization.models import Organization
    from services.api.src.workflow.models import Workflow


class AuditLog(Base):
    """Database model for tracking system-level audit logs."""

    __tablename__ = "audit_logs"

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
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # Auth, User, Org, Doc, OCR, AI, Workflow, Search, Report, Notification, Security
    severity: Mapped[str] = mapped_column(
        String(20),
        default="INFO",
        nullable=False,
        index=True,
    )  # Info, Warning, Error, Critical
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    resource_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    resource_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ocr_job_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ocr_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ai_job_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ai_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("workflows.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="SUCCESS",
        nullable=False,
    )
    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )
    details: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=lambda: {},
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="AuditLog.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="AuditLog.organization_id == Organization.id",
    )
    document: Mapped["Document | None"] = relationship(
        "Document",
        primaryjoin="AuditLog.document_id == Document.id",
    )
    ocr_job: Mapped["OCRJob | None"] = relationship(
        "OCRJob",
        primaryjoin="AuditLog.ocr_job_id == OCRJob.id",
    )
    ai_job: Mapped["AIJob | None"] = relationship(
        "AIJob",
        primaryjoin="AuditLog.ai_job_id == AIJob.id",
    )
    workflow: Mapped["Workflow | None"] = relationship(
        "Workflow",
        primaryjoin="AuditLog.workflow_id == Workflow.id",
    )


class ActivityLog(Base):
    """Database model for tracking detailed user activities on resource timelines."""

    __tablename__ = "activity_logs"

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
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    resource_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ocr_job_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ocr_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ai_job_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ai_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("workflows.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    details: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=lambda: {},
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        primaryjoin="ActivityLog.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="ActivityLog.organization_id == Organization.id",
    )
    document: Mapped["Document | None"] = relationship(
        "Document",
        primaryjoin="ActivityLog.document_id == Document.id",
    )
    ocr_job: Mapped["OCRJob | None"] = relationship(
        "OCRJob",
        primaryjoin="ActivityLog.ocr_job_id == OCRJob.id",
    )
    ai_job: Mapped["AIJob | None"] = relationship(
        "AIJob",
        primaryjoin="ActivityLog.ai_job_id == AIJob.id",
    )
    workflow: Mapped["Workflow | None"] = relationship(
        "Workflow",
        primaryjoin="ActivityLog.workflow_id == Workflow.id",
    )


class SecurityEvent(Base):
    """Database model for tracking security events and authentication history."""

    __tablename__ = "security_events"

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
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # failed_login, unauthorized_access, brute_force, credentials_change
    severity: Mapped[str] = mapped_column(
        String(20),
        default="INFO",
        nullable=False,
        index=True,
    )  # Info, Warning, Error, Critical
    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )
    metadata_log: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        default=lambda: {},
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    user: Mapped["User | None"] = relationship(
        "User",
        primaryjoin="SecurityEvent.user_id == User.id",
    )
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        primaryjoin="SecurityEvent.organization_id == Organization.id",
    )
