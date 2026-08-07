import logging
from datetime import UTC, datetime, timedelta
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workflow.models import SLA

logger = logging.getLogger(__name__)


class SLAManager:
    """SLA Manager managing response and resolution time targets, breach detection, and auto-escalations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_sla_target(
        self, lead_id: uuid.UUID, response_hours: int = 4, resolution_hours: int = 24
    ) -> SLA:
        now = datetime.now(UTC)
        sla = SLA(
            id=uuid.uuid4(),
            lead_id=lead_id,
            response_due_at=now + timedelta(hours=response_hours),
            resolution_due_at=now + timedelta(hours=resolution_hours),
            is_response_breached=False,
            is_resolution_breached=False,
            created_at=now,
        )
        self.db.add(sla)
        await self.db.commit()
        return sla

    async def evaluate_sla_breaches(self, sla: SLA) -> dict[str, bool]:
        now = datetime.now(UTC)
        if now > sla.response_due_at:
            sla.is_response_breached = True
        if now > sla.resolution_due_at:
            sla.is_resolution_breached = True
        await self.db.commit()
        return {
            "response_breached": sla.is_response_breached,
            "resolution_breached": sla.is_resolution_breached,
        }
