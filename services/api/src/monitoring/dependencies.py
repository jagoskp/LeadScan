# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.monitoring.repository import MonitoringRepository
from services.api.src.monitoring.service import HealthAggregationService


def get_monitoring_repository(
    session: AsyncSession = Depends(get_db),
) -> MonitoringRepository:
    """Inject MonitoringRepository context."""
    return MonitoringRepository(session)


def get_health_aggregation_service(
    repo: MonitoringRepository = Depends(get_monitoring_repository),
) -> HealthAggregationService:
    """Inject HealthAggregationService context."""
    return HealthAggregationService(repo)
