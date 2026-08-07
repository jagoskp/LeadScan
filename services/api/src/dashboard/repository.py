import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.dashboard.models import Dashboard, DashboardPreference, ReportDefinition

logger = logging.getLogger(__name__)


class DashboardRepository:
    """Repository handling persistence operations for Dashboards, Widgets, Layouts, and Reports."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_dashboards(self) -> Sequence[Dashboard]:
        stmt = select(Dashboard).order_by(Dashboard.created_at.desc())
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def list_reports(self) -> Sequence[ReportDefinition]:
        stmt = select(ReportDefinition).order_by(ReportDefinition.created_at.desc())
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def get_user_preference(self, user_id: uuid.UUID) -> DashboardPreference | None:
        stmt = select(DashboardPreference).where(DashboardPreference.user_id == user_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()
