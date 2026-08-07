import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.reports.dependencies import get_report_service
from services.api.src.reports.schemas import (
    ReportHistoryResponse,
    ReportJobCreate,
    ReportJobResponse,
    ReportResponse,
    ReportUpdate,
)
from services.api.src.reports.service import ReportService

# Two separate routers for clean structure
jobs_router = APIRouter(
    prefix="/organizations/{org_id}/report-jobs", tags=["report-jobs"]
)
reports_router = APIRouter(prefix="/organizations/{org_id}/reports", tags=["reports"])


# --- Report Jobs Endpoints ---


@jobs_router.post(
    "",
    response_model=ReportJobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_report_job(
    org_id: uuid.UUID,
    data: ReportJobCreate,
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> Any:
    """Create a new report generation request job."""
    return await report_service.create_report_job(
        org_id=org_id,
        user_id=current_user.id,
        data=data,
    )


@jobs_router.get("/{job_id}", response_model=ReportJobResponse)
async def get_report_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> Any:
    """Retrieve details and status for a report generation job."""
    return await report_service.get_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


@jobs_router.get("", response_model=list[ReportJobResponse])
async def list_report_jobs(
    org_id: uuid.UUID,
    status: str | None = Query(
        None, description="Filter by job status (e.g. PENDING, RUNNING)"
    ),  # noqa: B008
    skip: int = Query(0, ge=0),  # noqa: B008
    limit: int = Query(100, ge=1, le=100),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> Any:
    """List report generation jobs under organization."""
    return await report_service.list_jobs(
        org_id=org_id,
        user_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit,
    )


@jobs_router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> None:
    """Delete/cancel a report generation job."""
    await report_service.delete_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


# --- Completed Reports Endpoints ---


@reports_router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    org_id: uuid.UUID,
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> Any:
    """Retrieve details for a completed report."""
    return await report_service.get_report(
        org_id=org_id,
        user_id=current_user.id,
        report_id=report_id,
    )


@reports_router.get("", response_model=list[ReportResponse])
async def list_reports(
    org_id: uuid.UUID,
    is_archived: bool | None = Query(
        None, description="Filter by archived status"
    ),  # noqa: B008
    skip: int = Query(0, ge=0),  # noqa: B008
    limit: int = Query(100, ge=1, le=100),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> Any:
    """List completed reports in organization workspace."""
    return await report_service.list_reports(
        org_id=org_id,
        user_id=current_user.id,
        is_archived=is_archived,
        skip=skip,
        limit=limit,
    )


@reports_router.patch("/{report_id}", response_model=ReportResponse)
async def patch_report(
    org_id: uuid.UUID,
    report_id: uuid.UUID,
    data: ReportUpdate,
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> Any:
    """Rename, archive, or restore a completed report."""
    return await report_service.patch_report(
        org_id=org_id,
        user_id=current_user.id,
        report_id=report_id,
        data=data,
    )


@reports_router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    org_id: uuid.UUID,
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> None:
    """Permanently delete a completed report."""
    await report_service.delete_report(
        org_id=org_id,
        user_id=current_user.id,
        report_id=report_id,
    )


@reports_router.get("/{report_id}/history", response_model=list[ReportHistoryResponse])
async def get_report_history(
    org_id: uuid.UUID,
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    report_service: ReportService = Depends(get_report_service),  # noqa: B008
) -> Any:
    """Retrieve audit history logs for specific report."""
    return await report_service.get_history(
        org_id=org_id,
        user_id=current_user.id,
        report_id=report_id,
    )
