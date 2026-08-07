import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.identity.models import (
    DuplicateMatch,
    IdentityProfile,
    IdentityScore,
    MergeConflict,
    MergeHistory,
    RollbackHistory,
)

logger = logging.getLogger(__name__)


class IdentityRepository:
    """Repository handling persistence operations for Identity Resolution & Smart Duplicate Engine."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_duplicate_matches(
        self, status: str = "pending", limit: int = 50
    ) -> Sequence[DuplicateMatch]:
        stmt = (
            select(DuplicateMatch)
            .where(DuplicateMatch.status == status)
            .order_by(DuplicateMatch.duplicate_score.desc())
            .limit(limit)
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def get_match_by_id(self, match_id: uuid.UUID) -> DuplicateMatch | None:
        stmt = select(DuplicateMatch).where(DuplicateMatch.id == match_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def list_merge_history(self, limit: int = 50) -> Sequence[MergeHistory]:
        stmt = select(MergeHistory).order_by(MergeHistory.merged_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return res.scalars().all()
