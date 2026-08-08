import time
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.monitoring.health import (
    ping_celery_worker,
    ping_database,
    ping_redis,
)
from services.api.src.monitoring.models import (
    DependencyStatus,
    MetricsSnapshot,
    ServiceStatus,
    SystemHealth,
)
from services.api.src.monitoring.repository import MonitoringRepository


class HealthAggregationService:
    """Service compiling health status reports across backend dependencies."""

    def __init__(self, repository: MonitoringRepository) -> None:
        self.repo = repository
        self.start_time = time.time()

    async def aggregate_health(self, session: AsyncSession) -> dict[str, Any]:
        """Aggregate health status reports across Database, Redis, and Celery."""
        # 1. Measure latency pings
        db_lat = await ping_database(session)
        redis_lat = await ping_redis()
        celery_state = await ping_celery_worker()

        # 2. Formulate Dependency states
        db_ok = db_lat >= 0
        redis_ok = redis_lat >= 0

        # Persist Dependency logs
        db_dep = DependencyStatus(
            dependency_name="database",
            status="UP" if db_ok else "DOWN",
            latency_ms=db_lat if db_ok else 0.0,
        )
        redis_dep = DependencyStatus(
            dependency_name="redis",
            status="UP" if redis_ok else "DOWN",
            latency_ms=redis_lat if redis_ok else 0.0,
        )
        celery_dep = DependencyStatus(
            dependency_name="celery",
            status="UP" if celery_state == "ACTIVE" else "DOWN",
            latency_ms=0.0,
        )

        try:
            await self.repo.create_dependency_status(db_dep)
            await self.repo.create_dependency_status(redis_dep)
            await self.repo.create_dependency_status(celery_dep)
        except Exception:
            pass

        # 3. Formulate Service states
        ocr_svc = ServiceStatus(
            service_name="OCR",
            status="ACTIVE" if celery_state == "ACTIVE" else "DEGRADED",
        )
        ai_svc = ServiceStatus(
            service_name="AI",
            status="ACTIVE" if celery_state == "ACTIVE" else "DEGRADED",
        )

        try:
            await self.repo.create_service_status(ocr_svc)
            await self.repo.create_service_status(ai_svc)
        except Exception:
            pass

        # 4. Formulate SystemHealth logs
        is_healthy = db_ok
        overall_status = "HEALTHY" if is_healthy else "UNHEALTHY"
        if is_healthy and celery_state != "ACTIVE":
            overall_status = "DEGRADED"

        uptime = int(time.time() - self.start_time)
        sys_health = SystemHealth(
            status=overall_status,
            uptime_seconds=uptime,
            cpu_usage_percent=12.5,  # Simulated baseline CPU
            memory_usage_percent=45.2,  # Simulated baseline Memory
        )
        try:
            await self.repo.create_system_health(sys_health)
        except Exception:
            pass

        # 5. Formulate MetricsSnapshot logs
        # Query queue size (simulated or direct)
        queue_size = 0
        try:
            from services.worker.src.health import WorkerHealthCheck

            q_sizes = await WorkerHealthCheck.get_queue_sizes()
            queue_size = sum(q_sizes.values())
        except Exception:
            pass

        metrics_snap = MetricsSnapshot(
            api_requests_count=100,
            average_duration_ms=25.0,
            db_latency_ms=db_lat if db_ok else 0.0,
            redis_latency_ms=redis_lat if redis_ok else 0.0,
            queue_depth=queue_size,
            metrics_data={},
        )
        try:
            await self.repo.create_metrics_snapshot(metrics_snap)
        except Exception:
            pass

        return {
            "status": overall_status,
            "uptime_seconds": uptime,
            "cpu_usage_percent": 12.5,
            "memory_usage_percent": 45.2,
            "dependencies": [
                {
                    "id": db_dep.id,
                    "dependency_name": db_dep.dependency_name,
                    "status": db_dep.status,
                    "latency_ms": db_dep.latency_ms,
                    "created_at": db_dep.created_at,
                },
                {
                    "id": redis_dep.id,
                    "dependency_name": redis_dep.dependency_name,
                    "status": redis_dep.status,
                    "latency_ms": redis_dep.latency_ms,
                    "created_at": redis_dep.created_at,
                },
                {
                    "id": celery_dep.id,
                    "dependency_name": celery_dep.dependency_name,
                    "status": celery_dep.status,
                    "latency_ms": celery_dep.latency_ms,
                    "created_at": celery_dep.created_at,
                },
            ],
            "services": [
                {
                    "id": ocr_svc.id,
                    "service_name": ocr_svc.service_name,
                    "status": ocr_svc.status,
                    "created_at": ocr_svc.created_at,
                },
                {
                    "id": ai_svc.id,
                    "service_name": ai_svc.service_name,
                    "status": ai_svc.status,
                    "created_at": ai_svc.created_at,
                },
            ],
        }
