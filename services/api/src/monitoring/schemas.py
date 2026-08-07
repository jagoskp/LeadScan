import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SystemHealthResponse(BaseModel):
    id: uuid.UUID
    status: str
    uptime_seconds: int
    cpu_usage_percent: float
    memory_usage_percent: float
    created_at: datetime

    class Config:
        from_attributes = True


class DependencyStatusResponse(BaseModel):
    id: uuid.UUID
    dependency_name: str
    status: str
    latency_ms: float
    created_at: datetime

    class Config:
        from_attributes = True


class ServiceStatusResponse(BaseModel):
    id: uuid.UUID
    service_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MetricsSnapshotResponse(BaseModel):
    id: uuid.UUID
    api_requests_count: int
    average_duration_ms: float
    db_latency_ms: float
    redis_latency_ms: float
    queue_depth: int
    metrics_data: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class HealthSummaryResponse(BaseModel):
    status: str = Field(..., description="Overall health check status")
    timestamp: datetime = Field(default_factory=datetime.now)
    uptime_seconds: int = Field(0, description="Uptime of the app API gateway")
    cpu_usage_percent: float = Field(0.0)
    memory_usage_percent: float = Field(0.0)
    dependencies: list[DependencyStatusResponse] = Field(default_factory=list)
    services: list[ServiceStatusResponse] = Field(default_factory=list)
