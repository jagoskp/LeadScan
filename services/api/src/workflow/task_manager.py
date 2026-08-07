import logging
from datetime import UTC, datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workflow.exceptions import TaskNotFoundException
from services.api.src.workflow.models import Task
from services.api.src.workflow.schemas import TaskCreateSchema, TaskSchema
from services.api.src.workflow.validators import validate_task_priority

logger = logging.getLogger(__name__)


class TaskManager:
    """Task Manager encapsulating task creation, completion, assignments, and status updates."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, req: TaskCreateSchema) -> Task:
        validate_task_priority(req.priority)
        now = datetime.now(UTC)
        task = Task(
            id=uuid.uuid4(),
            lead_id=req.lead_id,
            title=req.title,
            description=req.description,
            priority=req.priority,
            status="Pending",
            due_date=req.due_date,
            assignee_id=req.assignee_id,
            created_at=now,
            updated_at=now,
        )
        self.db.add(task)
        await self.db.commit()
        return task

    async def complete_task(self, task_id: uuid.UUID) -> Task:
        task = await self.db.get(Task, task_id)
        if not task:
            raise TaskNotFoundException(str(task_id))
        task.status = "Completed"
        task.updated_at = datetime.now(UTC)
        await self.db.commit()
        return task

    async def update_status(self, task_id: uuid.UUID, new_status: str) -> Task:
        task = await self.db.get(Task, task_id)
        if not task:
            raise TaskNotFoundException(str(task_id))
        task.status = new_status
        task.updated_at = datetime.now(UTC)
        await self.db.commit()
        return task
