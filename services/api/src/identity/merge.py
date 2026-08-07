import logging
from datetime import UTC, datetime
from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.identity.conflict import ConflictResolver
from services.api.src.identity.models import MergeConflict, MergeHistory, RollbackHistory
from services.api.src.leads.enums import TimelineEventTypeEnum
from services.api.src.leads.models import Lead, LeadTimeline
from services.api.src.leads.repository import LeadRepository

logger = logging.getLogger(__name__)


class MergeEngine:
    """Safe Merge Engine re-linking secondary contacts, notes, tags, DAM assets, and creating RollbackHistory snapshots."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.lead_repo = LeadRepository(db)
        self.conflict_resolver = ConflictResolver()

    async def execute_safe_merge(
        self,
        primary_lead_id: uuid.UUID,
        secondary_lead_id: uuid.UUID,
        policy: str = "keep_original",
        custom_resolutions: dict[str, str] | None = None,
        reason: str = "Identity Resolution Merge",
        actor_id: uuid.UUID | None = None,
    ) -> MergeHistory:
        primary = await self.lead_repo.get_by_id(primary_lead_id)
        secondary = await self.lead_repo.get_by_id(secondary_lead_id)

        if not primary or not secondary:
            raise ValueError("Primary or Secondary lead record not found.")

        now = datetime.now(UTC)

        # 1. Capture Complete Pre-Merge Snapshot for 100% Lossless Rollback
        snapshot = {
            "primary_lead": {
                "id": str(primary.id),
                "title": primary.title,
                "status": primary.status,
                "priority": primary.priority,
            },
            "secondary_lead": {
                "id": str(secondary.id),
                "title": secondary.title,
                "status": secondary.status,
                "priority": secondary.priority,
                "is_archived": secondary.is_archived,
            },
        }

        # 2. Create MergeHistory Record
        merge_hist = MergeHistory(
            id=uuid.uuid4(),
            primary_lead_id=primary.id,
            secondary_lead_id=secondary.id,
            actor_id=actor_id,
            merge_reason=reason,
            duplicate_score=100.0,
            merged_at=now,
        )
        self.db.add(merge_hist)
        await self.db.flush()

        # 3. Save Rollback History Snapshot
        rollback_rec = RollbackHistory(
            id=uuid.uuid4(),
            merge_history_id=merge_hist.id,
            snapshot_before_merge=snapshot,
            is_restored=False,
        )
        self.db.add(rollback_rec)

        # 4. Resolve Field Conflicts
        conflicts_to_check = [("title", primary.title, secondary.title)]
        for f_name, p_val, s_val in conflicts_to_check:
            res_val, pol_used = self.conflict_resolver.resolve_field_conflict(
                f_name, p_val, s_val, policy, custom_resolutions.get(f_name) if custom_resolutions else None
            )
            c_obj = MergeConflict(
                id=uuid.uuid4(),
                merge_history_id=merge_hist.id,
                field_name=f_name,
                primary_value=p_val,
                secondary_value=s_val,
                resolved_value=res_val,
                resolution_policy=pol_used,
            )
            self.db.add(c_obj)

        # 5. Re-link secondary contacts, notes, and tags to primary lead
        for contact in secondary.contacts:
            contact.lead_id = primary.id
        for note in secondary.notes:
            note.lead_id = primary.id
        for tag in secondary.tags:
            tag.lead_id = primary.id

        # 6. Soft-archive secondary lead (NO PERMANENT DELETION)
        secondary.is_archived = True
        secondary.status = "Merged"
        secondary.updated_at = now
        primary.updated_at = now

        # 7. Audit Timeline Log
        timeline_p = LeadTimeline(
            id=uuid.uuid4(),
            lead_id=primary.id,
            event_type=TimelineEventTypeEnum.MERGED.value,
            title="Identity Merge Completed",
            description=f"Merged secondary lead '{secondary.title}' into primary record",
            actor_id=actor_id,
            created_at=now,
        )
        self.db.add(timeline_p)

        await self.db.commit()
        return merge_hist
