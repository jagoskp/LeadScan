import logging
from datetime import UTC, datetime
from typing import Any
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.identity.exceptions import DuplicateMatchNotFoundException
from services.api.src.identity.matcher import IdentityMatcher
from services.api.src.identity.merge import MergeEngine
from services.api.src.identity.models import DuplicateMatch
from services.api.src.identity.repository import IdentityRepository
from services.api.src.identity.rollback import RollbackEngine
from services.api.src.identity.schemas import (
    DuplicateMatchSchema,
    MergeConflictSchema,
    MergeExecuteRequest,
    MergeHistorySchema,
    MergePreviewResponse,
    RollbackHistorySchema,
)
from services.api.src.identity.scorer import IdentityScorer
from services.api.src.leads.repository import LeadRepository

logger = logging.getLogger(__name__)


class IdentityService:
    """Facade Service for Enterprise Identity Resolution & Smart Duplicate Engine."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = IdentityRepository(db)
        self.lead_repo = LeadRepository(db)
        self.matcher = IdentityMatcher()
        self.scorer = IdentityScorer()
        self.merge_engine = MergeEngine(db)
        self.rollback_engine = RollbackEngine(db)

    async def scan_for_duplicates(self, limit: int = 50) -> list[DuplicateMatchSchema]:
        """Scan active Master Lead records and generate duplicate match suggestions."""
        leads = await self.lead_repo.list_leads(limit=limit)
        matches: list[DuplicateMatchSchema] = []

        now = datetime.now(UTC)
        for i in range(len(leads)):
            for j in range(i + 1, len(leads)):
                l_a = leads[i]
                l_b = leads[j]

                primary_contact_a = l_a.contacts[0] if l_a.contacts else None
                primary_contact_b = l_b.contacts[0] if l_b.contacts else None

                eval_a = {
                    "title": l_a.title,
                    "company_name": l_a.company.company_name if l_a.company else "",
                    "gst_number": l_a.company.gst_number if l_a.company else "",
                    "email": primary_contact_a.emails[0] if primary_contact_a and primary_contact_a.emails else "",
                    "phone": primary_contact_a.phones[0] if primary_contact_a and primary_contact_a.phones else "",
                }

                eval_b = {
                    "title": l_b.title,
                    "company_name": l_b.company.company_name if l_b.company else "",
                    "gst_number": l_b.company.gst_number if l_b.company else "",
                    "email": primary_contact_b.emails[0] if primary_contact_b and primary_contact_b.emails else "",
                    "phone": primary_contact_b.phones[0] if primary_contact_b and primary_contact_b.phones else "",
                }

                m_eval = self.matcher.evaluate_match(eval_a, eval_b)
                scores = self.scorer.compute_scores(m_eval)

                if scores["duplicate_score"] >= 50.0:
                    d_match = DuplicateMatch(
                        id=uuid.uuid4(),
                        primary_lead_id=l_a.id,
                        secondary_lead_id=l_b.id,
                        duplicate_score=scores["duplicate_score"],
                        confidence_score=scores["confidence_score"],
                        match_type=scores["match_type"],
                        confidence_level=scores["confidence_level"],
                        status="pending",
                        created_at=now,
                    )
                    self.db.add(d_match)
                    matches.append(DuplicateMatchSchema.model_validate(d_match))

        await self.db.commit()
        return matches

    async def get_merge_preview(
        self, primary_lead_id: uuid.UUID, secondary_lead_id: uuid.UUID
    ) -> MergePreviewResponse:
        primary = await self.lead_repo.get_by_id(primary_lead_id)
        secondary = await self.lead_repo.get_by_id(secondary_lead_id)

        if not primary or not secondary:
            raise ValueError("Primary or Secondary lead not found")

        conflicts: list[MergeConflictSchema] = []
        if primary.title != secondary.title:
            conflicts.append(
                MergeConflictSchema(
                    id=uuid.uuid4(),
                    field_name="title",
                    primary_value=primary.title,
                    secondary_value=secondary.title,
                    resolved_value=primary.title,
                    resolution_policy="keep_original",
                )
            )

        return MergePreviewResponse(
            primary_lead_id=primary.id,
            secondary_lead_id=secondary.id,
            primary_title=primary.title,
            secondary_title=secondary.title,
            conflicts=conflicts,
            has_conflicts=len(conflicts) > 0,
            duplicate_score=100.0,
            confidence_level="100%",
        )

    async def execute_merge(
        self, request: MergeExecuteRequest, actor_id: uuid.UUID | None = None
    ) -> MergeHistorySchema:
        merge_hist = await self.merge_engine.execute_safe_merge(
            primary_lead_id=request.primary_lead_id,
            secondary_lead_id=request.secondary_lead_ids[0],
            policy=request.resolution_policy,
            custom_resolutions=request.custom_field_resolutions,
            reason=request.reason,
            actor_id=actor_id,
        )
        return MergeHistorySchema.model_validate(merge_hist)

    async def rollback_merge(self, merge_history_id: uuid.UUID) -> RollbackHistorySchema:
        rb_rec = await self.rollback_engine.execute_rollback(merge_history_id)
        return RollbackHistorySchema.model_validate(rb_rec)

    async def list_duplicate_matches(
        self, status: str = "pending", limit: int = 50
    ) -> list[DuplicateMatchSchema]:
        list_matches = await self.repo.list_duplicate_matches(status, limit)
        return [DuplicateMatchSchema.model_validate(m) for m in list_matches]
