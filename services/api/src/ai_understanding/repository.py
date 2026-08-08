import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.ai_understanding.models import (
    AIUnknownEntity,
    DetectedEntity,
    EntityRelation,
    Keyword,
    UnderstandingJob,
    UnderstandingMetadata,
)


class UnderstandingJobRepository:
    """Repository handling persistence operations for semantic jobs."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, job: UnderstandingJob) -> UnderstandingJob:
        """Persist a new UnderstandingJob configuration."""
        self.session.add(job)
        await self.session.flush()
        return job

    async def get_by_id(self, job_id: uuid.UUID) -> UnderstandingJob | None:
        """Retrieve an AI job preloading entities, relations, and logs."""
        stmt = (
            select(UnderstandingJob)
            .where(UnderstandingJob.id == job_id)
            .options(
                selectinload(UnderstandingJob.entities),
                selectinload(UnderstandingJob.relations),
                selectinload(UnderstandingJob.keywords),
                selectinload(UnderstandingJob.unknown_entities),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_jobs(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[UnderstandingJob]:
        """List AI jobs filtered by user context and organization."""
        stmt = select(UnderstandingJob).options(
            selectinload(UnderstandingJob.entities),
        )
        filters = []
        if user_id:
            filters.append(UnderstandingJob.user_id == user_id)
        if organization_id:
            filters.append(UnderstandingJob.organization_id == organization_id)
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(
        self,
        job_id: uuid.UUID,
        status: str,
        document_type: str | None = None,
    ) -> UnderstandingJob | None:
        """Update job lifecycle status and classification results."""
        values: dict[str, Any] = {"status": status}
        if document_type is not None:
            values["document_type"] = document_type

        stmt = (
            update(UnderstandingJob)
            .where(UnderstandingJob.id == job_id)
            .values(**values)
        )
        await self.session.execute(stmt)
        return await self.get_by_id(job_id)

    async def delete(self, job_id: uuid.UUID) -> bool:
        """Delete an AI job by ID."""
        stmt = delete(UnderstandingJob).where(UnderstandingJob.id == job_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))


class DetectedEntityRepository:
    """Repository handling persistence operations for entities and graphs."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_entity(self, entity: DetectedEntity) -> DetectedEntity:
        """Persist a new DetectedEntity."""
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get_entity_by_id(self, entity_id: uuid.UUID) -> DetectedEntity | None:
        """Retrieve a specific entity by ID."""
        stmt = select(DetectedEntity).where(DetectedEntity.id == entity_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_relation(self, relation: EntityRelation) -> EntityRelation:
        """Persist a new EntityRelation link."""
        self.session.add(relation)
        await self.session.flush()
        return relation

    async def create_keyword(self, keyword: Keyword) -> Keyword:
        """Persist a new search Keyword tag."""
        self.session.add(keyword)
        await self.session.flush()
        return keyword

    async def create_unknown_entity(self, unknown: AIUnknownEntity) -> AIUnknownEntity:
        """Persist an AIUnknownEntity record to preserve unmapped text."""
        self.session.add(unknown)
        await self.session.flush()
        return unknown

    async def add_metadata(
        self, metadata: UnderstandingMetadata
    ) -> UnderstandingMetadata:
        """Persist an UnderstandingMetadata execution stat."""
        self.session.add(metadata)
        await self.session.flush()
        return metadata
