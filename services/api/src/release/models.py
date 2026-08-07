import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base


class ReleaseCertification(Base):
    """ReleaseCertification model storing production release candidate certification records."""

    __tablename__ = "release_certifications"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    release_version: Mapped[str] = mapped_column(
        String(50),
        default="1.0.0-RC1",
        nullable=False,
        index=True,
    )
    certification_status: Mapped[str] = mapped_column(
        String(30),
        default="CERTIFIED",
        nullable=False,
    )  # CERTIFIED, DEGRADED, FAILED
    audited_by: Mapped[str] = mapped_column(
        String(100),
        default="Enterprise Architect Auditor",
        nullable=False,
    )
    overall_score: Mapped[float] = mapped_column(
        Float,
        default=100.0,
        nullable=False,
    )
    certification_details: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class ProductionAuditLog(Base):
    """ProductionAuditLog model auditing production readiness checks and deployment events."""

    __tablename__ = "release_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    certification_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("release_certifications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )  # security, database, api, performance, devops, backup
    test_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="PASS",
        nullable=False,
    )  # PASS, FAIL, WARNING
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
