import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.api.src.ai.models import AIJob, AIResult


class AIRepository:
    """Repository managing AI database operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_job_by_id(self, job_id: uuid.UUID) -> AIJob | None:
        """Fetch AI Job by primary key, preloading its AIResult."""
        result = await self.session.execute(
            select(AIJob).options(joinedload(AIJob.result)).where(AIJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_job_by_id_and_org(
        self, job_id: uuid.UUID, org_id: uuid.UUID
    ) -> AIJob | None:
        """Fetch AI Job by ID and organization ID, preloading AIResult."""
        result = await self.session.execute(
            select(AIJob)
            .options(joinedload(AIJob.result))
            .where(
                AIJob.id == job_id,
                AIJob.organization_id == org_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_jobs_by_org(
        self,
        org_id: uuid.UUID,
        status: str | None = None,
        provider: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AIJob]:
        """List AI Jobs under an organization with optional filters."""
        stmt = (
            select(AIJob)
            .options(joinedload(AIJob.result))
            .where(AIJob.organization_id == org_id)
        )
        if status is not None:
            stmt = stmt.where(AIJob.status == status)
        if provider is not None:
            stmt = stmt.where(AIJob.provider == provider)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_job(self, job: AIJob) -> AIJob:
        """Persist a new AI Job record."""
        self.session.add(job)
        await self.session.flush()
        return job

    async def update_job(
        self, job_id: uuid.UUID, update_data: dict[str, Any]
    ) -> AIJob | None:
        """Modify fields on an existing AI Job."""
        if update_data:
            await self.session.execute(
                update(AIJob).where(AIJob.id == job_id).values(**update_data)
            )
        return await self.get_job_by_id(job_id)

    async def delete_job(self, job_id: uuid.UUID) -> None:
        """Permanently delete an AI Job (cascade deletes AIResult)."""
        await self.session.execute(delete(AIJob).where(AIJob.id == job_id))

    async def create_result(self, ai_result: AIResult) -> AIResult:
        """Persist a new AI Result record."""
        self.session.add(ai_result)
        await self.session.flush()
        return ai_result

    async def delete_result_by_job_id(self, job_id: uuid.UUID) -> None:
        """Permanently delete the AI Result associated with a job ID."""
        await self.session.execute(delete(AIResult).where(AIResult.job_id == job_id))


class_variable_preventer = None
