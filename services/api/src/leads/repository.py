import logging
from typing import Sequence
import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.leads.models import (
    Company,
    Contact,
    Lead,
    LeadHistory,
    LeadMetadata,
    LeadNote,
    LeadTag,
    LeadTimeline,
)

logger = logging.getLogger(__name__)


class LeadRepository:
    """Repository handling persistence operations for Enterprise Lead Repository data models."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, lead_id: uuid.UUID) -> Lead | None:
        stmt = (
            select(Lead)
            .options(
                selectinload(Lead.company),
                selectinload(Lead.contacts),
                selectinload(Lead.tags),
                selectinload(Lead.notes),
                selectinload(Lead.lead_metadata),
                selectinload(Lead.timeline_records),
            )
            .where(Lead.id == lead_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def list_leads(
        self,
        search_query: str | None = None,
        status: str | None = None,
        is_archived: bool = False,
        limit: int = 50,
    ) -> Sequence[Lead]:
        stmt = (
            select(Lead)
            .options(
                selectinload(Lead.company),
                selectinload(Lead.contacts),
                selectinload(Lead.tags),
            )
            .where(Lead.is_archived == is_archived)
        )

        if status:
            stmt = stmt.where(Lead.status == status)

        if search_query:
            term = f"%{search_query}%"
            stmt = stmt.join(Company, isouter=True).join(Contact, isouter=True).where(
                or_(
                    Lead.title.ilike(term),
                    Company.company_name.ilike(term),
                    Company.gst_number.ilike(term),
                    Contact.first_name.ilike(term),
                    Contact.last_name.ilike(term),
                )
            ).distinct()

        stmt = stmt.order_by(Lead.updated_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_company_by_name(self, company_name: str) -> Company | None:
        stmt = select(Company).where(Company.company_name == company_name)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_timeline(self, lead_id: uuid.UUID) -> Sequence[LeadTimeline]:
        stmt = (
            select(LeadTimeline)
            .where(LeadTimeline.lead_id == lead_id)
            .order_by(LeadTimeline.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
