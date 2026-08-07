import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.dashboard.schemas import (
    AnalyticsResponse,
    CommandCenterTelemetryResponse,
    ReportCreateSchema,
    ReportSchema,
    SystemHealthItem,
)
from services.api.src.dashboard.service import DashboardService
from services.api.src.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/dashboard", tags=["Enterprise Command Center Dashboard & Analytics Platform"])


@router.get("/telemetry", response_model=CommandCenterTelemetryResponse)
async def get_command_center_telemetry(db: AsyncSession = Depends(get_db)):
    """Get real-time operational control center telemetry across all modules."""
    service = DashboardService(db)
    return await service.get_telemetry()


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(db: AsyncSession = Depends(get_db)):
    """Get Lead Funnel, Conversion Rate, Sync Success, and Duplicate analytics."""
    service = DashboardService(db)
    return await service.get_analytics()


@router.get("/health", response_model=list[SystemHealthItem])
async def get_system_health(db: AsyncSession = Depends(get_db)):
    """Get live system health telemetry for DB, Search, Storage, and Queues."""
    service = DashboardService(db)
    return await service.health_monitor.get_system_health()


@router.get("/reports", response_model=list[ReportSchema])
async def list_reports(db: AsyncSession = Depends(get_db)):
    """List saved analytical report definitions."""
    service = DashboardService(db)
    return await service.list_reports()


@router.post("/reports", response_model=ReportSchema, status_code=status.HTTP_201_CREATED)
async def create_report(
    payload: ReportCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create custom analytical report definition."""
    service = DashboardService(db)
    return await service.create_report(payload)
