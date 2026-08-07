import logging
from datetime import UTC, datetime, timedelta
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workflow.models import Reminder

logger = logging.getLogger(__name__)


class ReminderEngine:
    """Reminder Engine managing task reminders, snooze, dismiss, and reschedule logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def schedule_reminder(self, task_id: uuid.UUID, reminder_time: datetime) -> Reminder:
        now = datetime.now(UTC)
        rem = Reminder(
            id=uuid.uuid4(),
            task_id=task_id,
            reminder_time=reminder_time,
            is_triggered=False,
            is_snoozed=False,
            created_at=now,
        )
        self.db.add(rem)
        await self.db.commit()
        return rem

    async def snooze_reminder(self, reminder_id: uuid.UUID, snooze_minutes: int = 15) -> Reminder:
        rem = await self.db.get(Reminder, reminder_id)
        if not rem:
            raise ValueError("Reminder not found")
        rem.is_snoozed = True
        rem.snooze_until = datetime.now(UTC) + timedelta(minutes=snooze_minutes)
        await self.db.commit()
        return rem
