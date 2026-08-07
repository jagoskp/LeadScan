import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.release.models import ReleaseCertification

logger = logging.getLogger(__name__)


class ReleaseRepository:
    """Repository handling persistence operations for Release Certification records."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_latest_certification(self) -> ReleaseCertification | None:
        stmt = select(ReleaseCertification).order_by(ReleaseCertification.created_at.desc())
        res = await self.db.execute(stmt)
        return res.scalars().first()
