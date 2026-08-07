import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class KPICard(BaseModel):
    title: str
    value: str | int | float
    change_pct: float = 0.0
    trend: str = "up"  # up, down, neutral
    icon: str = "chart"


class LiveMonitorItem(BaseModel):
    queue_name: str
    active_count: int
    pending_count: int
    failed_count: int
    status: str = "healthy"


class SystemHealthItem(BaseModel):
    component: str
    status: str  # operational, degraded, outage
    latency_ms: float
    last_check_at: datetime


class CommandCenterTelemetryResponse(BaseModel):
    todays_scans: int
    todays_leads: int
    pending_reviews: int
    pending_workflows: int
    google_sync_status: str
    storage_usage_mb: float
    kpi_cards: list[KPICard]
    live_monitors: list[LiveMonitorItem]
    system_health: list[SystemHealthItem]


class AnalyticsFunnelStage(BaseModel):
    stage_name: str
    count: int
    conversion_pct: float


class AnalyticsResponse(BaseModel):
    total_leads: int
    conversion_rate: float
    sync_success_rate: float
    duplicate_rate: float
    funnel: list[AnalyticsFunnelStage]


class ReportCreateSchema(BaseModel):
    name: str
    report_type: str = "lead_summary"
    date_range: str = "daily"
    filters: dict[str, Any] = {}


class ReportSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    report_type: str
    date_range: str
    filters: dict[str, Any] | None = None
    created_at: datetime


class DashboardWidgetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    dashboard_id: uuid.UUID
    widget_type: str
    title: str
    config: dict[str, Any] | None = None
    col_span: int
    row_span: int


class DashboardSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    dashboard_type: str
    is_default: bool
    created_at: datetime
    widgets: list[DashboardWidgetSchema] = []
