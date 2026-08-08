import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.monitoring.metrics import AppMetrics


async def ping_database(session: AsyncSession) -> float:
    """Measure ping latency to the PostgreSQL database in milliseconds."""
    start = time.perf_counter()
    try:
        # Run a simple query to assert DB session connection
        await session.execute(select(1))
        latency = (time.perf_counter() - start) * 1000.0
        AppMetrics.update_db_latency(latency)
        return latency
    except Exception:
        AppMetrics.update_db_latency(-1.0)
        return -1.0


async def ping_redis() -> float:
    """Measure ping latency to the Redis connection broker in milliseconds."""
    from leadscan_config import AppSettings

    settings = AppSettings()
    if not settings.REDIS_URL:
        AppMetrics.update_redis_latency(-1.0)
        return -1.0

    start = time.perf_counter()
    try:
        import redis

        client = redis.from_url(settings.REDIS_URL)
        client.ping()
        latency = (time.perf_counter() - start) * 1000.0
        AppMetrics.update_redis_latency(latency)
        return latency
    except Exception:
        AppMetrics.update_redis_latency(-1.0)
        return -1.0


async def ping_celery_worker() -> str:
    """Verify Celery workers status."""
    try:
        from services.worker.src.celery_app import celery_app

        inspector = celery_app.control.inspect()
        pings = inspector.ping()
        if pings:
            return "ACTIVE"
        return "INACTIVE"
    except Exception:
        return "UNAVAILABLE"
