# ruff: noqa: B008
from services.worker.src.dispatcher import TaskDispatcher
from services.worker.src.health import WorkerHealthCheck


def get_task_dispatcher() -> TaskDispatcher:
    """Inject TaskDispatcher service instance."""
    return TaskDispatcher()


def get_worker_health_check() -> type[WorkerHealthCheck]:
    """Inject WorkerHealthCheck context class type."""
    return WorkerHealthCheck
