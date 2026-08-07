import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from services.api.src.database import Base


class SystemHealth(Base):
    """Database model for storing historical system resource health logs."""

    __tablename__ = "monitoring_system_health"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="HEALTHY",
        nullable=False,
    )  # HEALTHY, DEGRADED, UNHEALTHY
    uptime_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    cpu_usage_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    memory_usage_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class DependencyStatus(Base):
    """Database model for logging latency and ping states of backend dependencies."""

    __tablename__ = "monitoring_dependency_status"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    dependency_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # database, redis, celery
    status: Mapped[str] = mapped_column(
        String(20),
        default="UP",
        nullable=False,
    )  # UP, DOWN, DEGRADED
    latency_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class ServiceStatus(Base):
    """Database model for tracking overall health status of system modules."""

    __tablename__ = "monitoring_service_status"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    service_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # OCR, AI, Search, Notification, Workflow, Storage, Audit, Reports
    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",
        nullable=False,
    )  # ACTIVE, INACTIVE, DEGRADED
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class MetricsSnapshot(Base):
    """Database model storing snapshots of application metrics."""

    __tablename__ = "monitoring_metrics_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    api_requests_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    average_duration_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    db_latency_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    redis_latency_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    queue_depth: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    metrics_data: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=lambda: {},
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
