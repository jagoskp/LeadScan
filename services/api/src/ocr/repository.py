import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.api.src.ocr.models import OCRJob, OCRResult


class OCRRepository:
    """Repository managing OCR database operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_job_by_id(self, job_id: uuid.UUID) -> OCRJob | None:
        """Fetch OCR Job by primary key, preloading its OCRResult."""
        result = await self.session.execute(
            select(OCRJob).options(joinedload(OCRJob.result)).where(OCRJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_job_by_id_and_org(
        self, job_id: uuid.UUID, org_id: uuid.UUID
    ) -> OCRJob | None:
        """Fetch OCR Job by ID and organization ID, preloading OCRResult."""
        result = await self.session.execute(
            select(OCRJob)
            .options(joinedload(OCRJob.result))
            .where(
                OCRJob.id == job_id,
                OCRJob.organization_id == org_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_jobs_by_org(
        self,
        org_id: uuid.UUID,
        status: str | None = None,
        engine: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[OCRJob]:
        """List OCR Jobs under an organization with optional filters."""
        stmt = (
            select(OCRJob)
            .options(joinedload(OCRJob.result))
            .where(OCRJob.organization_id == org_id)
        )
        if status is not None:
            stmt = stmt.where(OCRJob.status == status)
        if engine is not None:
            stmt = stmt.where(OCRJob.engine == engine)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_job(self, job: OCRJob) -> OCRJob:
        """Persist a new OCR Job record."""
        self.session.add(job)
        await self.session.flush()
        return job

    async def update_job(
        self, job_id: uuid.UUID, update_data: dict[str, Any]
    ) -> OCRJob | None:
        """Modify fields on an existing OCR Job."""
        if update_data:
            await self.session.execute(
                update(OCRJob).where(OCRJob.id == job_id).values(**update_data)
            )
        return await self.get_job_by_id(job_id)

    async def delete_job(self, job_id: uuid.UUID) -> None:
        """Permanently delete an OCR Job (cascade deletes OCRResult)."""
        await self.session.execute(delete(OCRJob).where(OCRJob.id == job_id))

    async def get_result_by_job_id(self, job_id: uuid.UUID) -> OCRResult | None:
        """Fetch OCRResult associated with a specific job ID."""
        result = await self.session.execute(
            select(OCRResult).where(OCRResult.job_id == job_id)
        )
        return result.scalar_one_or_none()

    async def create_result(self, ocr_result: OCRResult) -> OCRResult:
        """Persist a new OCR Result record."""
        self.session.add(ocr_result)
        await self.session.flush()
        return ocr_result

    async def delete_result_by_job_id(self, job_id: uuid.UUID) -> None:
        """Permanently delete the OCR Result associated with a job ID."""
        await self.session.execute(delete(OCRResult).where(OCRResult.job_id == job_id))
