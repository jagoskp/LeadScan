import logging
from typing import Any
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workflow.automation import AutomationDispatcher
from services.api.src.workflow.models import Workflow
from services.api.src.workflow.interfaces import IWorkflowEngine

logger = logging.getLogger(__name__)


class WorkflowEngine(IWorkflowEngine):
    """Workflow Engine evaluating active workflows on event triggers."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.dispatcher = AutomationDispatcher(db)

    async def trigger_event(self, event_name: str, payload: dict[str, Any]) -> list[str]:
        stmt = select(Workflow).where(Workflow.trigger_type == event_name, Workflow.is_active.is_(True))
        res = await self.db.execute(stmt)
        active_workflows = res.scalars().all()

        executed_actions: list[str] = []
        lead_id = payload.get("lead_id")
        if isinstance(lead_id, str):
            lead_id = uuid.UUID(lead_id)

        for wf in active_workflows:
            for rule in wf.rules:
                action = await self.dispatcher.execute_rule(rule, lead_id, payload)
                executed_actions.append(action)

        return executed_actions
