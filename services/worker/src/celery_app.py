import asyncio
import os
from typing import Any

from celery import Celery

from services.worker.src.queue import task_queues

# Broker & Backend Redis connection URL
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "leadscan",
    broker=redis_url,
    backend=redis_url,
)

# Update configuration parameters
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_default_queue="default",
    task_queues=task_queues,
    # Configure task routing maps
    task_routes={
        "ocr.*": {"queue": "ocr"},
        "ai.*": {"queue": "ai"},
        "search.*": {"queue": "search"},
        "report.*": {"queue": "report"},
        "notification.*": {"queue": "notification"},
        "workflow.*": {"queue": "workflow"},
        "maintenance.*": {"queue": "maintenance"},
    },
    # Ensure tasks are acknowledged after execution completes
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)  # type: ignore[untyped-decorator]
def execute_registered_task(
    self: Any, task_name: str, *args: Any, **kwargs: Any
) -> Any:
    """Generic proxy task routing Celery executions to TaskRegistry handlers."""
    from services.worker.src.registry import TaskRegistry

    handler = TaskRegistry.get_handler(task_name)
    try:
        # Run the async execute method inside an event loop
        return asyncio.run(handler.execute(*args, **kwargs))
    except Exception as exc:
        # Standard retry strategy backing off upon exceptions
        raise self.retry(exc=exc) from exc
