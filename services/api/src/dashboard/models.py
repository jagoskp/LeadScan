import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.src.database import Base


class Dashboard(Base):
    """Dashboard model defining layout configurations for role-based views."""

    __tablename__ = "dashboards"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    dashboard_type: Mapped[str] = mapped_column(
        String(50),
        default="executive",
        nullable=False,
    )  # executive, operations, lead, workflow, google_sheets, search, asset, identity, system
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    widgets: Mapped[list["DashboardWidget"]] = relationship(
        "DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan"
    )


class DashboardWidget(Base):
    """DashboardWidget model configuring individual dynamic dashboard widgets."""

    __tablename__ = "dashboard_widgets"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    dashboard_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dashboards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    widget_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # kpi_cards, live_monitor, lead_funnel, sync_status, system_health, workflow_queue
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    config: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    col_span: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    row_span: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    dashboard: Mapped["Dashboard"] = relationship("Dashboard", back_populates="widgets")


class DashboardLayout(Base):
    """DashboardLayout model storing drag-and-drop grid arrangements."""

    __tablename__ = "dashboard_layouts"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    dashboard_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dashboards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    grid_layout: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class DashboardPreference(Base):
    """DashboardPreference model managing dark/light mode and layout preferences."""

    __tablename__ = "dashboard_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    theme_mode: Mapped[str] = mapped_column(
        String(20),
        default="dark",
        nullable=False,
    )  # dark, light, system
    auto_refresh_seconds: Mapped[int] = mapped_column(
        Integer,
        default=30,
        nullable=False,
    )


class AnalyticsSnapshot(Base):
    """AnalyticsSnapshot model storing aggregated platform performance metrics."""

    __tablename__ = "analytics_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    metric_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )  # lead_conversion_rate, ocr_accuracy, sync_success_rate, duplicate_rate
    metric_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    dimensions: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    snapshot_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )


class ReportDefinition(Base):
    """ReportDefinition model managing saved custom analytical reports."""

    __tablename__ = "report_definitions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    report_type: Mapped[str] = mapped_column(
        String(50),
        default="lead_summary",
        nullable=False,
    )  # lead_summary, sync_history, ocr_performance, workflow_audit
    date_range: Mapped[str] = mapped_column(
        String(50),
        default="daily",
        nullable=False,
    )  # daily, weekly, monthly, yearly, custom
    filters: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
