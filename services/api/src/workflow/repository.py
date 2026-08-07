import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workflow.models import SLA, FollowUp, NotificationQueue, Reminder, Task, Workflow

logger = logging.getLogger(__name__)


class WorkflowRepository:
    """Repository handling persistence operations for Workflow, Task, Reminder, FollowUp, and SLA."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_workflows(self) -> Sequence[Workflow]:
        stmt = select(Workflow).order_by(Workflow.created_at.desc())
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def list_tasks(
        self, lead_id: uuid.UUID | None = None, status: str | None = None, limit: int = 50
    ) -> Sequence[Task]:
        stmt = select(Task)
        if lead_id:
            stmt = stmt.where(Task.lead_id == lead_id)
        if status:
            stmt = stmt.where(Task.status == status)
        stmt = stmt.order_by(Task.due_date.asc().nulls_last()).limit(limit)
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def list_followups(self, lead_id: uuid.UUID | None = None) -> Sequence[FollowUp]:
        stmt = select(FollowUp)
        if lead_id:
            stmt = stmt.where(FollowUp.lead_id == lead_id)
        stmt = stmt.order_by(FollowUp.scheduled_at.asc())
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def get_sla_by_lead(self, lead_id: uuid.UUID) -> SLA | None:
        stmt = select(SLA).where(SLA.lead_id == lead_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()
