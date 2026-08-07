from typing import Any

from services.worker.src.exceptions import TaskRegistrationException
from services.worker.src.interfaces import ITaskHandler


class TaskRegistry:
    """Registry managing registrations of logical task names to concrete handlers."""

    _tasks: dict[str, ITaskHandler] = {}

    @classmethod
    def register(cls, task_name: str, handler: ITaskHandler) -> None:
        """Bind a task name to an implementation handler instance."""
        if task_name in cls._tasks:
            raise TaskRegistrationException(
                f"Task '{task_name}' is already registered."
            )
        cls._tasks[task_name] = handler

    @classmethod
    def get_handler(cls, task_name: str) -> ITaskHandler:
        """Fetch the registered handler for a task name."""
        if task_name not in cls._tasks:
            raise TaskRegistrationException(
                f"Task handler for '{task_name}' is not registered."
            )
        return cls._tasks[task_name]

    @classmethod
    def clear(cls) -> None:
        """Clear all task registrations."""
        cls._tasks.clear()


class WorkerRegistry:
    """Registry tracking active background worker metadata configurations."""

    _workers: dict[str, dict[str, Any]] = {}

    @classmethod
    def register_node(cls, node_id: str, metadata: dict[str, Any]) -> None:
        """Record configuration settings of a worker node."""
        cls._workers[node_id] = metadata

    @classmethod
    def get_node(cls, node_id: str) -> dict[str, Any] | None:
        """Retrieve settings configuration for a worker node."""
        return cls._workers.get(node_id)

    @classmethod
    def list_nodes(cls) -> dict[str, dict[str, Any]]:
        """List all registered worker nodes."""
        return cls._workers
