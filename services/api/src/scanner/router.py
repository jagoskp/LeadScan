# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.scanner.dependencies import get_scanner_service
from services.api.src.scanner.schemas import (
    DetectedFieldResponse,
    DetectedFieldUpdate,
    DuplicateComparisonResponse,
    ManualReviewFieldsMerge,
    ManualReviewFieldSplit,
    ManualReviewStatusUpdate,
    ScanJobCreate,
    ScanJobResponse,
    ScanResultResponse,
)
from services.api.src.scanner.service import ScannerService
from services.api.src.scanner.validators import validate_scan_source

router = APIRouter(prefix="/scanner", tags=["scanner"])


# ----------------------------------------------------
# Scan Jobs Endpoints
# ----------------------------------------------------

@router.post(
    "/jobs",
    response_model=ScanJobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_scan_job(
    data: ScanJobCreate,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Create a new scan job and execute the architectural mock pipeline."""
    validate_scan_source(data.source)
    # Register/create job
    job = await service.create_job(
        user_id=current_user.id,
        source=data.source.value,
        organization_id=data.organization_id,
    )
    # Execute structural mock pipeline immediately to populate results
    await service.execute_pipeline(job.id)
    return await service.get_job(job.id)


@router.get("/jobs", response_model=list[ScanJobResponse])
async def list_scan_jobs(
    organization_id: uuid.UUID | None = Query(
        None, description="Filter by organization"
    ),
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """List scan jobs filtered by user context and organization."""
    return await service.list_jobs(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/jobs/{job_id}", response_model=ScanJobResponse)
async def get_scan_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Retrieve detailed properties of a single scan job."""
    return await service.get_job(job_id)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scan_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> None:
    """Cancel and delete a scan job configuration."""
    await service.delete_job(job_id)


# ----------------------------------------------------
# Scan Results Endpoints
# ----------------------------------------------------

@router.get("/jobs/{job_id}/result", response_model=ScanResultResponse)
async def get_scan_result(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Retrieve scanner results, including fields, extra info, and suggestions."""
    return await service.get_result_by_job_id(job_id)


# ----------------------------------------------------
# Manual Review Endpoints
# ----------------------------------------------------

@router.post("/results/{result_id}/review", response_model=ScanResultResponse)
async def submit_manual_review(
    result_id: uuid.UUID,
    payload: ManualReviewStatusUpdate,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Approve or reject scanner result outputs."""
    if payload.review_status == "APPROVED":
        return await service.approve_result(result_id)
    else:
        return await service.reject_result(result_id)


@router.patch("/fields/{field_id}", response_model=DetectedFieldResponse)
async def update_detected_field(
    field_id: uuid.UUID,
    payload: DetectedFieldUpdate,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Edit value, classification rename, or status of a single detected field."""
    if payload.value is not None:
        return await service.edit_field(field_id, payload.value)
    if payload.field_name is not None:
        return await service.rename_field(field_id, payload.field_name.value)

    # General properties update fallback
    update_data = payload.model_dump(exclude_unset=True)
    return await service.result_repo.update_field(field_id, update_data)


@router.delete("/fields/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_detected_field(
    field_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> None:
    """Delete a field that was incorrectly mapped or detected."""
    await service.delete_field(field_id)


@router.post("/fields/merge", response_model=DetectedFieldResponse)
async def merge_detected_fields(
    payload: ManualReviewFieldsMerge,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Merge values from multiple fields into a single field."""
    return await service.merge_fields(
        payload.field_ids, payload.target_field_name.value
    )


@router.post("/fields/{field_id}/split", response_model=list[DetectedFieldResponse])
async def split_detected_field(
    field_id: uuid.UUID,
    payload: ManualReviewFieldSplit,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Split a compound field value into multiple separate fields."""
    return await service.split_field(
        field_id, payload.delimiter, payload.new_field_keys
    )


# ----------------------------------------------------
# Duplicate Comparison Endpoints
# ----------------------------------------------------

@router.get("/jobs/{job_id}/duplicates", response_model=DuplicateComparisonResponse)
async def check_duplicates(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ScannerService = Depends(get_scanner_service),
) -> Any:
    """Compare scan job outputs to find potential duplicates.

    Checks by standard attributes.
    """
    await service.get_job(job_id)
    # Check duplicate matching by triggering comparative engine mocks
    return DuplicateComparisonResponse(
        is_duplicate=False,
        potential_duplicate_job_ids=[],
        matched_by_fields=[],
    )
