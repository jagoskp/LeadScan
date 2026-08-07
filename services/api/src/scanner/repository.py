import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.scanner.models import (
    DetectedField,
    ScanJob,
    ScanResult,
)


class ScanJobRepository:
    """Repository handling persistence operations for ScanJobs, images, and metadata."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, job: ScanJob) -> ScanJob:
        """Persist a new ScanJob."""
        self.session.add(job)
        await self.session.flush()
        return job

    async def get_by_id(self, job_id: uuid.UUID) -> ScanJob | None:
        """Retrieve a ScanJob by ID, preloading images, AI suggestions, and metadata."""
        stmt = (
            select(ScanJob)
            .where(ScanJob.id == job_id)
            .options(
                selectinload(ScanJob.images),
                selectinload(ScanJob.ai_suggestions),
                selectinload(ScanJob.metadata_records),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_jobs(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[ScanJob]:
        """List jobs matching the user or organization scope."""
        stmt = select(ScanJob).options(
            selectinload(ScanJob.images),
            selectinload(ScanJob.ai_suggestions),
            selectinload(ScanJob.metadata_records),
        )
        filters = []
        if user_id:
            filters.append(ScanJob.user_id == user_id)
        if organization_id:
            filters.append(ScanJob.organization_id == organization_id)
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(self, job_id: uuid.UUID, status: str) -> ScanJob | None:
        """Update job status fields."""
        stmt = (
            update(ScanJob)
            .where(ScanJob.id == job_id)
            .values(status=status)
        )
        await self.session.execute(stmt)
        return await self.get_by_id(job_id)

    async def delete(self, job_id: uuid.UUID) -> bool:
        """Delete a ScanJob by ID."""
        stmt = delete(ScanJob).where(ScanJob.id == job_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))


class ScanResultRepository:
    """Repository handling persistence operations for ScanResult and fields."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_result(self, result: ScanResult) -> ScanResult:
        """Persist a new ScanResult."""
        self.session.add(result)
        await self.session.flush()
        return result

    async def get_by_job_id(self, job_id: uuid.UUID) -> ScanResult | None:
        """Retrieve a ScanResult by its Job ID, preloading relations."""
        stmt = (
            select(ScanResult)
            .where(ScanResult.job_id == job_id)
            .options(
                selectinload(ScanResult.detected_fields),
                selectinload(ScanResult.extra_information),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, result_id: uuid.UUID) -> ScanResult | None:
        """Retrieve a ScanResult by ID, preloading fields and extra info."""
        stmt = (
            select(ScanResult)
            .where(ScanResult.id == result_id)
            .options(
                selectinload(ScanResult.detected_fields),
                selectinload(ScanResult.extra_information),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_result(
        self, result_id: uuid.UUID, data: dict[str, Any]
    ) -> ScanResult | None:
        """Update result fields (e.g. confidence score, logo status, review status)."""
        if data:
            stmt = (
                update(ScanResult)
                .where(ScanResult.id == result_id)
                .values(**data)
            )
            await self.session.execute(stmt)
        return await self.get_by_id(result_id)

    async def get_field_by_id(self, field_id: uuid.UUID) -> DetectedField | None:
        """Retrieve a specific DetectedField."""
        stmt = select(DetectedField).where(DetectedField.id == field_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_field(self, field: DetectedField) -> DetectedField:
        """Persist a new DetectedField."""
        self.session.add(field)
        await self.session.flush()
        return field

    async def update_field(
        self, field_id: uuid.UUID, data: dict[str, Any]
    ) -> DetectedField | None:
        """Update field properties."""
        if data:
            stmt = (
                update(DetectedField)
                .where(DetectedField.id == field_id)
                .values(**data)
            )
            await self.session.execute(stmt)
        return await self.get_field_by_id(field_id)

    async def delete_field(self, field_id: uuid.UUID) -> bool:
        """Delete a DetectedField."""
        stmt = delete(DetectedField).where(DetectedField.id == field_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))
