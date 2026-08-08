import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.sync_engine.models import (
    ConnectorProfile,
    SyncConnector,
    SyncHistory,
    SyncJob,
    SyncResult,
)


class ConnectorRepository:
    """Repository handling persistence operations for connector integrations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_connector(self, connector: SyncConnector) -> SyncConnector:
        """Persist a new SyncConnector definition."""
        self.session.add(connector)
        await self.session.flush()
        return connector

    async def get_connector_by_id(
        self, connector_id: uuid.UUID
    ) -> SyncConnector | None:
        """Retrieve a specific SyncConnector by ID."""
        stmt = (
            select(SyncConnector)
            .where(SyncConnector.id == connector_id)
            .options(selectinload(SyncConnector.profiles))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_connectors(self) -> Sequence[SyncConnector]:
        """Fetch all active target SyncConnectors."""
        stmt = (
            select(SyncConnector)
            .where(SyncConnector.is_active.is_(True))
            .options(selectinload(SyncConnector.profiles))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_profile(
        self, profile: ConnectorProfile
    ) -> ConnectorProfile:
        """Persist ConnectorProfile configurations."""
        self.session.add(profile)
        await self.session.flush()
        return profile

    async def get_profile_by_id(
        self, profile_id: uuid.UUID
    ) -> ConnectorProfile | None:
        """Retrieve ConnectorProfile preloading credentials and metadata."""
        stmt = (
            select(ConnectorProfile)
            .where(ConnectorProfile.id == profile_id)
            .options(
                selectinload(ConnectorProfile.credentials),
                selectinload(ConnectorProfile.metadata_records),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class SyncJobRepository:
    """Repository handling persistence operations for SyncQueue jobs."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_job(self, job: SyncJob) -> SyncJob:
        """Persist a new SyncJob configuration."""
        self.session.add(job)
        await self.session.flush()
        return job

    async def get_job_by_id(self, job_id: uuid.UUID) -> SyncJob | None:
        """Retrieve SyncJob preloading history logs."""
        stmt = (
            select(SyncJob)
            .where(SyncJob.id == job_id)
            .options(selectinload(SyncJob.history_logs))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_job_status(
        self, job_id: uuid.UUID, status: str, retry_inc: bool = False
    ) -> SyncJob | None:
        """Update SyncJob queue status and retry counts."""
        job = await self.get_job_by_id(job_id)
        if not job:
            return None

        values: dict[str, Any] = {"status": status}
        if retry_inc:
            values["retry_count"] = job.retry_count + 1

        stmt = update(SyncJob).where(SyncJob.id == job_id).values(**values)
        await self.session.execute(stmt)
        return await self.get_job_by_id(job_id)

    async def create_history(self, history: SyncHistory) -> SyncHistory:
        """Persist SyncHistory logging attempts."""
        self.session.add(history)
        await self.session.flush()
        return history

    async def create_result(self, result: SyncResult) -> SyncResult:
        """Persist SyncResult response snapshots."""
        self.session.add(result)
        await self.session.flush()
        return result

    async def get_failed_jobs(self) -> Sequence[SyncJob]:
        """Retrieve SyncJobs in failed status that are retry eligible."""
        stmt = (
            select(SyncJob)
            .where(
                and_(
                    SyncJob.status == "Failed",
                    SyncJob.retry_count < SyncJob.max_retries,
                )
            )
            .options(selectinload(SyncJob.history_logs))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
