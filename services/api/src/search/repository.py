import logging
from datetime import UTC, datetime
from typing import Any, Sequence
import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.leads.models import Company, Contact, Lead, LeadNote
from services.api.src.search.models import SavedSearch, SearchHistory, SearchIndex

logger = logging.getLogger(__name__)


class SearchRepository:
    """Repository handling persistence operations for Universal Search indices, saved searches, and history."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def global_query_indices(
        self,
        search_term: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Query SearchIndex, Lead, Contact, Company, and LeadNote records for global search matches."""
        term = f"%{search_term}%"

        # 1. Search Leads & Companies & Contacts
        lead_stmt = (
            select(Lead)
            .join(Company, isouter=True)
            .join(Contact, isouter=True)
            .where(
                or_(
                    Lead.title.ilike(term),
                    Company.company_name.ilike(term),
                    Company.gst_number.ilike(term),
                    Contact.first_name.ilike(term),
                    Contact.last_name.ilike(term),
                )
            )
            .distinct()
            .limit(limit)
        )

        res = await self.db.execute(lead_stmt)
        leads = res.scalars().all()

        results: list[dict[str, Any]] = []

        for l in leads:
            primary_contact = l.contacts[0] if l.contacts else None
            results.append(
                {
                    "id": l.id,
                    "lead_id": l.id,
                    "company_id": l.company_id,
                    "contact_id": primary_contact.id if primary_contact else None,
                    "title": l.title,
                    "company_name": l.company.company_name if l.company else None,
                    "gst_number": l.company.gst_number if l.company else None,
                    "email": primary_contact.emails[0] if primary_contact and primary_contact.emails else None,
                    "phone": primary_contact.phones[0] if primary_contact and primary_contact.phones else None,
                    "source_type": "Lead Repository",
                    "created_at": l.created_at,
                    "status": l.status,
                }
            )

        return results

    async def log_search_history(
        self, user_id: uuid.UUID, query: str, filters: dict | None, count: int
    ) -> SearchHistory:
        hist = SearchHistory(
            id=uuid.uuid4(),
            user_id=user_id,
            query_string=query,
            filters=filters,
            results_count=count,
            created_at=datetime.now(UTC),
        )
        self.db.add(hist)
        await self.db.commit()
        return hist

    async def list_recent_searches(self, user_id: uuid.UUID, limit: int = 10) -> Sequence[SearchHistory]:
        stmt = (
            select(SearchHistory)
            .where(SearchHistory.user_id == user_id)
            .order_by(SearchHistory.created_at.desc())
            .limit(limit)
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def save_search(
        self, user_id: uuid.UUID, title: str, query: str, filters: dict | None, is_pinned: bool = False
    ) -> SavedSearch:
        saved = SavedSearch(
            id=uuid.uuid4(),
            user_id=user_id,
            title=title,
            query_string=query,
            filters=filters,
            is_pinned=is_pinned,
            created_at=datetime.now(UTC),
        )
        self.db.add(saved)
        await self.db.commit()
        return saved

    async def list_saved_searches(self, user_id: uuid.UUID) -> Sequence[SavedSearch]:
        stmt = (
            select(SavedSearch)
            .where(SavedSearch.user_id == user_id)
            .order_by(SavedSearch.is_pinned.desc(), SavedSearch.created_at.desc())
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()
