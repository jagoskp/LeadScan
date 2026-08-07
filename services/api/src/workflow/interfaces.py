from abc import ABC, abstractmethod
from typing import Any
import uuid

from services.api.src.workflow.schemas import TaskCreateSchema, TaskSchema


class ITaskManager(ABC):

    @abstractmethod
    async def create_task(self, req: TaskCreateSchema) -> TaskSchema:
        pass

    @abstractmethod
    async def complete_task(self, task_id: uuid.UUID) -> TaskSchema:
        pass


class IWorkflowEngine(ABC):

    @abstractmethod
    async def trigger_event(self, event_name: str, payload: dict[str, Any]) -> list[str]:
        pass
