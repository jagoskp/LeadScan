import uuid
from collections.abc import Sequence
from typing import Any

from services.api.src.organization.exceptions import (
    ForbiddenOrganizationActionException,
)
from services.api.src.organization.repository import OrganizationMemberRepository
from services.api.src.reports.exceptions import (
    ReportJobNotFoundException,
    ReportNotFoundException,
)
from services.api.src.reports.models import Report, ReportHistory, ReportJob
from services.api.src.reports.repository import ReportRepository
from services.api.src.reports.schemas import ReportJobCreate, ReportUpdate


class ReportService:
    """Service coordinates Report metadata and generation job lifecycles."""

    def __init__(
        self,
        report_repo: ReportRepository,
        member_repo: OrganizationMemberRepository,
    ) -> None:
        self.report_repo = report_repo
        self.member_repo = member_repo

    async def _verify_org_membership(
        self, org_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """Validate user membership inside organization."""
        member = await self.member_repo.get_member(org_id, user_id)
        if not member:
            raise ForbiddenOrganizationActionException()

    async def create_report_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        data: ReportJobCreate,
    ) -> ReportJob:
        """Create new Report generation job with pending state."""
        await self._verify_org_membership(org_id, user_id)

        job = ReportJob(
            name=data.name,
            report_type=data.report_type,
            organization_id=org_id,
            owner_id=user_id,
            filters=data.filters.model_dump(),
            export_format=data.export_format,
            status="PENDING",
        )
        saved = await self.report_repo.create_job(job)

        # Log creation history audit
        history = ReportHistory(
            report_job_id=saved.id,
            organization_id=org_id,
            user_id=user_id,
            action="JOB_CREATED",
            details={
                "name": data.name,
                "report_type": data.report_type,
                "export_format": data.export_format,
            },
        )
        await self.report_repo.create_history_entry(history)

        return saved

    async def get_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> ReportJob:
        """Retrieve details of specific report generation job."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.report_repo.get_job_by_id(job_id, org_id)
        if not job:
            raise ReportJobNotFoundException()
        return job

    async def list_jobs(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ReportJob]:
        """List report generation jobs under organization."""
        await self._verify_org_membership(org_id, user_id)
        return await self.report_repo.list_jobs_by_org(
            org_id=org_id, status=status, skip=skip, limit=limit
        )

    async def delete_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> None:
        """Permanently delete/cancel a report generation job."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.report_repo.get_job_by_id(job_id, org_id)
        if not job:
            raise ReportJobNotFoundException()

        await self.report_repo.delete_job(job_id)

    async def get_report(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        report_id: uuid.UUID,
    ) -> Report:
        """Retrieve details of completed report. Validates org access."""
        await self._verify_org_membership(org_id, user_id)

        report = await self.report_repo.get_report_by_id(report_id, org_id)
        if not report:
            raise ReportNotFoundException()
        return report

    async def list_reports(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        is_archived: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Report]:
        """List reports in organization."""
        await self._verify_org_membership(org_id, user_id)
        return await self.report_repo.list_reports_by_org(
            org_id=org_id, is_archived=is_archived, skip=skip, limit=limit
        )

    async def patch_report(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        report_id: uuid.UUID,
        data: ReportUpdate,
    ) -> Report:
        """Update, archive, or restore completed report."""
        await self._verify_org_membership(org_id, user_id)

        report = await self.report_repo.get_report_by_id(report_id, org_id)
        if not report:
            raise ReportNotFoundException()

        update_dict: dict[str, Any] = {}
        history_actions = []

        if data.name is not None:
            update_dict["name"] = data.name
            history_actions.append(
                ReportHistory(
                    report_id=report_id,
                    organization_id=org_id,
                    user_id=user_id,
                    action="REPORT_RENAMED",
                    details={"old_name": report.name, "new_name": data.name},
                )
            )

        if data.is_archived is not None:
            update_dict["is_archived"] = data.is_archived
            action = "REPORT_ARCHIVED" if data.is_archived else "REPORT_RESTORED"
            history_actions.append(
                ReportHistory(
                    report_id=report_id,
                    organization_id=org_id,
                    user_id=user_id,
                    action=action,
                    details={"is_archived": data.is_archived},
                )
            )

        updated = await self.report_repo.update_report(report_id, update_dict)
        if not updated:
            raise ReportNotFoundException()

        # Log audit history entries
        for hist in history_actions:
            await self.report_repo.create_history_entry(hist)

        return updated

    async def delete_report(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        report_id: uuid.UUID,
    ) -> None:
        """Delete report metadata. Logs action in audit trail."""
        await self._verify_org_membership(org_id, user_id)

        report = await self.report_repo.get_report_by_id(report_id, org_id)
        if not report:
            raise ReportNotFoundException()

        await self.report_repo.delete_report(report_id)

        # Log deletion audit log (log record stays in report_histories)
        history = ReportHistory(
            report_id=report_id,
            organization_id=org_id,
            user_id=user_id,
            action="REPORT_DELETED",
            details={"name": report.name},
        )
        await self.report_repo.create_history_entry(history)

    async def get_history(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        report_id: uuid.UUID,
    ) -> Sequence[ReportHistory]:
        """Fetch audit trail log logs for specific report."""
        await self._verify_org_membership(org_id, user_id)
        return await self.report_repo.get_history_by_report(report_id, org_id)
