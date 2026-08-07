import logging
from datetime import UTC, datetime
from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workflow.exceptions import TaskNotFoundException, WorkflowNotFoundException
from services.api.src.workflow.models import FollowUp, Workflow, WorkflowRule
from services.api.src.workflow.repository import WorkflowRepository
from services.api.src.workflow.schemas import (
    FollowUpCreateSchema,
    FollowUpSchema,
    ReminderSchema,
    SLASchema,
    TaskCreateSchema,
    TaskSchema,
    WorkflowCreateSchema,
    WorkflowSchema,
)
from services.api.src.workflow.sla import SLAManager
from services.api.src.workflow.task_manager import TaskManager
from services.api.src.workflow.workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)


class WorkflowService:
    """Facade Application Service for Enterprise Workflow Automation Engine."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = WorkflowRepository(db)
        self.task_manager = TaskManager(db)
        self.sla_manager = SLAManager(db)
        self.engine = WorkflowEngine(db)

    async def create_workflow(self, req: WorkflowCreateSchema) -> WorkflowSchema:
        wf = Workflow(
            id=uuid.uuid4(),
            name=req.name,
            trigger_type=req.trigger_type,
            is_active=req.is_active,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        self.db.add(wf)
        await self.db.commit()
        return WorkflowSchema.model_validate(wf)

    async def list_workflows(self) -> list[WorkflowSchema]:
        wfs = await self.repo.list_workflows()
        return [WorkflowSchema.model_validate(w) for w in wfs]

    async def create_task(self, req: TaskCreateSchema) -> TaskSchema:
        t_obj = await self.task_manager.create_task(req)
        return TaskSchema.model_validate(t_obj)

    async def complete_task(self, task_id: uuid.UUID) -> TaskSchema:
        t_obj = await self.task_manager.complete_task(task_id)
        return TaskSchema.model_validate(t_obj)

    async def list_tasks(
        self, lead_id: uuid.UUID | None = None, status: str | None = None, limit: int = 50
    ) -> list[TaskSchema]:
        tasks = await self.repo.list_tasks(lead_id, status, limit)
        return [TaskSchema.model_validate(t) for t in tasks]

    async def schedule_followup(self, req: FollowUpCreateSchema) -> FollowUpSchema:
        f_obj = FollowUp(
            id=uuid.uuid4(),
            lead_id=req.lead_id,
            follow_up_type=req.follow_up_type,
            summary=req.summary,
            notes=req.notes,
            scheduled_at=req.scheduled_at,
            is_completed=False,
            created_at=datetime.now(UTC),
        )
        self.db.add(f_obj)
        await self.db.commit()
        return FollowUpSchema.model_validate(f_obj)

    async def list_followups(self, lead_id: uuid.UUID | None = None) -> list[FollowUpSchema]:
        fus = await self.repo.list_followups(lead_id)
        return [FollowUpSchema.model_validate(f) for f in fus]

    async def create_sla_target(self, lead_id: uuid.UUID) -> SLASchema:
        sla_obj = await self.sla_manager.create_sla_target(lead_id)
        return SLASchema.model_validate(sla_obj)
