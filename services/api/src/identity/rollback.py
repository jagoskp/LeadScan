import logging
from datetime import UTC, datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.identity.exceptions import RollbackFailedException
from services.api.src.identity.models import MergeHistory, RollbackHistory
from services.api.src.leads.enums import TimelineEventTypeEnum
from services.api.src.leads.models import Lead, LeadTimeline

logger = logging.getLogger(__name__)


class RollbackEngine:
    """Rollback Engine restoring pre-merge snapshots and un-archiving secondary leads."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_rollback(self, merge_history_id: uuid.UUID) -> RollbackHistory:
        stmt = select(RollbackHistory).where(RollbackHistory.merge_history_id == merge_history_id)
        res = await self.db.execute(stmt)
        rollback_rec = res.scalars().first()

        if not rollback_rec:
            raise RollbackFailedException(f"Rollback snapshot for merge '{merge_history_id}' not found.")
        if rollback_rec.is_restored:
            raise RollbackFailedException(f"Merge '{merge_history_id}' has already been rolled back.")

        snapshot = rollback_rec.snapshot_before_merge
        sec_snapshot = snapshot.get("secondary_lead", {})
        sec_id = sec_snapshot.get("id")

        if sec_id:
            sec_uuid = uuid.UUID(sec_id)
            sec_lead = await self.db.get(Lead, sec_uuid)
            if sec_lead:
                sec_lead.is_archived = False
                sec_lead.status = sec_snapshot.get("status", "New")
                sec_lead.updated_at = datetime.now(UTC)

                # Log timeline
                t_obj = LeadTimeline(
                    id=uuid.uuid4(),
                    lead_id=sec_lead.id,
                    event_type=TimelineEventTypeEnum.RESTORED.value,
                    title="Merge Rollback Restored Lead",
                    description="Record restored from merge rollback snapshot",
                    created_at=datetime.now(UTC),
                )
                self.db.add(t_obj)

        rollback_rec.is_restored = True
        rollback_rec.restored_at = datetime.now(UTC)

        await self.db.commit()
        return rollback_rec
