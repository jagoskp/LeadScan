import uuid
from collections.abc import Sequence

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.ocr_engine.models import (
    OCRBlock,
    OCREngineJob,
    OCRLine,
    OCRMetadata,
    OCRPage,
    OCRWord,
)


class OCRJobRepository:
    """Repository handling persistence operations for OCREngineJobs and metadata."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, job: OCREngineJob) -> OCREngineJob:
        """Persist a new OCREngineJob."""
        self.session.add(job)
        await self.session.flush()
        return job

    async def get_by_id(self, job_id: uuid.UUID) -> OCREngineJob | None:
        """Retrieve a specific OCREngineJob preloading page extraction hierarchies."""
        stmt = (
            select(OCREngineJob)
            .where(OCREngineJob.id == job_id)
            .options(
                selectinload(OCREngineJob.pages).selectinload(OCRPage.blocks),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_jobs(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[OCREngineJob]:
        """List OCR requests matching the user/organization scope."""
        stmt = select(OCREngineJob).options(
            selectinload(OCREngineJob.pages),
        )
        filters = []
        if user_id:
            filters.append(OCREngineJob.user_id == user_id)
        if organization_id:
            filters.append(OCREngineJob.organization_id == organization_id)
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(self, job_id: uuid.UUID, status: str) -> OCREngineJob | None:
        """Update job lifecycle status."""
        stmt = (
            update(OCREngineJob)
            .where(OCREngineJob.id == job_id)
            .values(status=status)
        )
        await self.session.execute(stmt)
        return await self.get_by_id(job_id)

    async def delete(self, job_id: uuid.UUID) -> bool:
        """Delete an OCREngineJob by ID."""
        stmt = delete(OCREngineJob).where(OCREngineJob.id == job_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))


class OCRPageRepository:
    """Repository handling persistence operations for OCRPage layout hierarchies."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_page(self, page: OCRPage) -> OCRPage:
        """Persist a new OCRPage."""
        self.session.add(page)
        await self.session.flush()
        return page

    async def get_page_by_id(self, page_id: uuid.UUID) -> OCRPage | None:
        """Retrieve page details with complete blocks/lines/words preloaded."""
        stmt = (
            select(OCRPage)
            .where(OCRPage.id == page_id)
            .options(
                selectinload(OCRPage.blocks)
                .selectinload(OCRBlock.lines)
                .selectinload(OCRLine.words)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_pages_by_job_id(self, job_id: uuid.UUID) -> Sequence[OCRPage]:
        """Fetch all pages associated with a target Job ID."""
        stmt = (
            select(OCRPage)
            .where(OCRPage.job_id == job_id)
            .options(
                selectinload(OCRPage.blocks)
                .selectinload(OCRBlock.lines)
                .selectinload(OCRLine.words)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_block(self, block: OCRBlock) -> OCRBlock:
        """Persist a new OCRBlock."""
        self.session.add(block)
        await self.session.flush()
        return block

    async def create_line(self, line: OCRLine) -> OCRLine:
        """Persist a new OCRLine."""
        self.session.add(line)
        await self.session.flush()
        return line

    async def create_word(self, word: OCRWord) -> OCRWord:
        """Persist a new OCRWord."""
        self.session.add(word)
        await self.session.flush()
        return word

    async def add_metadata(self, metadata: OCRMetadata) -> OCRMetadata:
        """Persist an OCRMetadata record."""
        self.session.add(metadata)
        await self.session.flush()
        return metadata
