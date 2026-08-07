import logging
from datetime import UTC, datetime
from typing import Any
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.search.models import SearchIndex, SearchMetadata

logger = logging.getLogger(__name__)


class SearchIndexer:
    """Incremental & Background Indexing Engine for Lead, Contact, Company, OCR, and AI extractions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def index_lead_record(
        self,
        lead_id: uuid.UUID,
        title: str,
        company_name: str | None = None,
        gst_number: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        tags: list[str] | None = None,
        raw_text: str | None = None,
    ) -> SearchIndex:
        """Create or update SearchIndex record for a Lead."""
        now = datetime.now(UTC)
        stmt = select(SearchIndex).where(SearchIndex.lead_id == lead_id)
        res = await self.db.execute(stmt)
        idx_obj = res.scalars().first()

        if not idx_obj:
            idx_obj = SearchIndex(
                id=uuid.uuid4(),
                lead_id=lead_id,
                title=title,
                company_name=company_name,
                gst_number=gst_number,
                email=email,
                phone=phone,
                content_text=raw_text or f"{title} {company_name or ''} {gst_number or ''}",
                tags=tags or [],
                file_type="lead",
                created_at=now,
                updated_at=now,
            )
            self.db.add(idx_obj)
        else:
            idx_obj.title = title
            idx_obj.company_name = company_name
            idx_obj.gst_number = gst_number
            idx_obj.email = email
            idx_obj.phone = phone
            idx_obj.tags = tags or []
            idx_obj.content_text = raw_text or f"{title} {company_name or ''}"
            idx_obj.updated_at = now

        await self.db.commit()
        return idx_obj
