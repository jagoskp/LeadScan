import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.reports.models import Report, ReportHistory, ReportJob


class ReportRepository:
    """Repository managing Reporting & Analytics database operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_report_by_id(
        self, report_id: uuid.UUID, org_id: uuid.UUID
    ) -> Report | None:
        """Fetch Report by ID and organization ID."""
        result = await self.session.execute(
            select(Report).where(
                Report.id == report_id,
                Report.organization_id == org_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_reports_by_org(
        self,
        org_id: uuid.UUID,
        is_archived: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Report]:
        """List reports under an organization with optional archived filter."""
        stmt = select(Report).where(Report.organization_id == org_id)
        if is_archived is not None:
            stmt = stmt.where(Report.is_archived == is_archived)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_report(self, report: Report) -> Report:
        """Persist a new Report record."""
        self.session.add(report)
        await self.session.flush()
        return report

    async def update_report(
        self, report_id: uuid.UUID, update_data: dict[str, Any]
    ) -> Report | None:
        """Modify fields on an existing Report record."""
        if update_data:
            await self.session.execute(
                update(Report).where(Report.id == report_id).values(**update_data)
            )
        # Fetch fresh
        result = await self.session.execute(
            select(Report).where(Report.id == report_id)
        )
        return result.scalar_one_or_none()

    async def delete_report(self, report_id: uuid.UUID) -> None:
        """Permanently delete a Report record (history logs remain)."""
        await self.session.execute(delete(Report).where(Report.id == report_id))

    async def get_job_by_id(
        self, job_id: uuid.UUID, org_id: uuid.UUID
    ) -> ReportJob | None:
        """Fetch ReportJob by ID and organization ID."""
        result = await self.session.execute(
            select(ReportJob).where(
                ReportJob.id == job_id,
                ReportJob.organization_id == org_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_jobs_by_org(
        self,
        org_id: uuid.UUID,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ReportJob]:
        """List ReportJobs under an organization workspace."""
        stmt = select(ReportJob).where(ReportJob.organization_id == org_id)
        if status is not None:
            stmt = stmt.where(ReportJob.status == status)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_job(self, job: ReportJob) -> ReportJob:
        """Persist a new ReportJob record."""
        self.session.add(job)
        await self.session.flush()
        return job

    async def update_job(
        self, job_id: uuid.UUID, update_data: dict[str, Any]
    ) -> ReportJob | None:
        """Modify status/fields on an existing ReportJob."""
        if update_data:
            await self.session.execute(
                update(ReportJob).where(ReportJob.id == job_id).values(**update_data)
            )
        # Fetch fresh
        result = await self.session.execute(
            select(ReportJob).where(ReportJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def delete_job(self, job_id: uuid.UUID) -> None:
        """Permanently delete a ReportJob (used to cancel pending/queued jobs)."""
        await self.session.execute(delete(ReportJob).where(ReportJob.id == job_id))

    async def create_history_entry(self, history: ReportHistory) -> ReportHistory:
        """Persist a ReportHistory audit log entry."""
        self.session.add(history)
        await self.session.flush()
        return history

    async def get_history_by_report(
        self, report_id: uuid.UUID, org_id: uuid.UUID
    ) -> Sequence[ReportHistory]:
        """Fetch audit log history entries associated with a report."""
        stmt = (
            select(ReportHistory)
            .where(
                ReportHistory.report_id == report_id,
                ReportHistory.organization_id == org_id,
            )
            .order_by(desc(ReportHistory.created_at))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
