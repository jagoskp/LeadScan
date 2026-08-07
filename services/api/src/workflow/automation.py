import logging
from datetime import UTC, datetime
from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workflow.models import AutomationLog, NotificationQueue, WorkflowRule
from services.api.src.workflow.task_manager import TaskManager
from services.api.src.workflow.schemas import TaskCreateSchema

logger = logging.getLogger(__name__)


class AutomationDispatcher:
    """Automation Dispatcher evaluating workflow rules and dispatching automated actions."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_manager = TaskManager(db)

    async def execute_rule(self, rule: WorkflowRule, lead_id: uuid.UUID | None, context: dict[str, Any]) -> str:
        action = rule.action_type
        if action == "create_task":
            await self.task_manager.create_task(
                TaskCreateSchema(
                    title=f"Automated Follow-up for {context.get('title', 'Lead')}",
                    lead_id=lead_id,
                    priority="High",
                )
            )
        elif action == "send_notification":
            notif = NotificationQueue(
                id=uuid.uuid4(),
                channel="in_app",
                recipient=context.get("owner_email", "admin@leadscan.ai"),
                message=f"Automation triggered: {rule.condition_field} matched {rule.condition_value}",
                status="queued",
                created_at=datetime.now(UTC),
            )
            self.db.add(notif)

        log_obj = AutomationLog(
            id=uuid.uuid4(),
            workflow_id=rule.workflow_id,
            lead_id=lead_id,
            action_taken=action,
            details={"condition": rule.condition_field, "value": rule.condition_value},
            created_at=datetime.now(UTC),
        )
        self.db.add(log_obj)
        await self.db.commit()
        return action
