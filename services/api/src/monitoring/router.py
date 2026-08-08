# ruff: noqa: B008
from typing import Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.monitoring.dependencies import (
    get_health_aggregation_service,
)
from services.api.src.monitoring.exceptions import (
    DependencyUnavailableException,
)
from services.api.src.monitoring.health import ping_database, ping_redis
from services.api.src.monitoring.metrics import AppMetrics
from services.api.src.monitoring.schemas import HealthSummaryResponse
from services.api.src.monitoring.service import HealthAggregationService

router = APIRouter(prefix="/health", tags=["monitoring"])


@router.get("", response_model=HealthSummaryResponse)
async def get_health_summary(
    db_session: AsyncSession = Depends(get_db),
    service: HealthAggregationService = Depends(get_health_aggregation_service),
) -> Any:
    """Retrieve detailed system and dependencies health status summary."""
    return await service.aggregate_health(db_session)


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_probe() -> dict[str, str]:
    """Liveness probe checking if the API gateway container is running."""
    return {"status": "ALIVE"}


@router.get("/ready")
async def readiness_probe(
    db_session: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Readiness probe checking if the API gateway is ready to serve requests."""
    db_lat = await ping_database(db_session)
    _ = await ping_redis()

    if db_lat < 0:
        raise DependencyUnavailableException(
            "Ready check failed: database connection unavailable."
        )

    return {"status": "READY"}


@router.get("/metrics")
async def get_prometheus_metrics() -> Response:
    """Scrape endpoint rendering Prometheus compatible metric formats."""
    metrics_text = AppMetrics.to_prometheus_format()
    return Response(content=metrics_text, media_type="text/plain")
