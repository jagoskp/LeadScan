import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.documents.models import Document


class DocumentRepository:
    """Repository managing Document database persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, doc_id: uuid.UUID) -> Document | None:
        """Fetch a Document record by its primary key ID."""
        result = await self.session.execute(
            select(Document).where(Document.id == doc_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_and_org(
        self, doc_id: uuid.UUID, org_id: uuid.UUID
    ) -> Document | None:
        """Fetch a Document record by its ID and organization ID key."""
        result = await self.session.execute(
            select(Document).where(
                Document.id == doc_id,
                Document.organization_id == org_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_org(
        self,
        org_id: uuid.UUID,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Document]:
        """List all documents under an organization with optional status filter."""
        stmt = select(Document).where(Document.organization_id == org_id)
        if status is not None:
            stmt = stmt.where(Document.status == status)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, document: Document) -> Document:
        """Persist a new Document metadata model instance."""
        self.session.add(document)
        await self.session.flush()
        return document

    async def update(
        self, doc_id: uuid.UUID, update_data: dict[str, Any]
    ) -> Document | None:
        """Update metadata attributes on a Document by its primary ID key."""
        if update_data:
            await self.session.execute(
                update(Document).where(Document.id == doc_id).values(**update_data)
            )
        return await self.get_by_id(doc_id)

    async def delete(self, doc_id: uuid.UUID) -> None:
        """Permanently delete a Document record by its ID key."""
        await self.session.execute(
            delete(Document).where(Document.id == doc_id)
        )

    async def search_by_org(
        self,
        org_id: uuid.UUID,
        query: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Document]:
        """Search documents by matching query against filename or original filename."""
        pattern = f"%{query}%"
        stmt = (
            select(Document)
            .where(
                Document.organization_id == org_id,
                or_(
                    Document.filename.ilike(pattern),
                    Document.original_filename.ilike(pattern),
                ),
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
