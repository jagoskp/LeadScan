from typing import Any

from services.worker.src.celery_app import execute_registered_task
from services.worker.src.exceptions import TaskDispatchException


class TaskDispatcher:
    """Dispatcher enqueuing tasks into the Celery message broker."""

    def dispatch_task(
        self,
        task_name: str,
        args: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
        countdown: int | None = None,
        queue: str | None = None,
    ) -> str:
        """Asynchronously dispatch a background task, returning the Celery task ID."""
        try:
            task_args = [task_name] + list(args or [])
            task_kwargs = kwargs or {}

            options: dict[str, Any] = {}
            if countdown is not None:
                options["countdown"] = countdown
            if queue is not None:
                options["queue"] = queue

            result = execute_registered_task.apply_async(
                args=task_args,
                kwargs=task_kwargs,
                **options,
            )
            return str(result.id)
        except Exception as exc:
            raise TaskDispatchException(
                f"Failed to dispatch task '{task_name}': {exc}"
            ) from exc
