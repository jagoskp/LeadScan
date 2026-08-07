from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.organization.dependencies import (
    get_organization_member_repository,
)
from services.api.src.organization.repository import OrganizationMemberRepository
from services.api.src.reports.repository import ReportRepository
from services.api.src.reports.service import ReportService


def get_report_repository(
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> ReportRepository:
    """Inject ReportRepository context."""
    return ReportRepository(session)


def get_report_service(
    report_repo: ReportRepository = Depends(get_report_repository),  # noqa: B008
    member_repo: OrganizationMemberRepository = Depends(  # noqa: B008
        get_organization_member_repository
    ),
) -> ReportService:
    """Inject ReportService context."""
    return ReportService(report_repo, member_repo)
