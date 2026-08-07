import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.ocr.dependencies import get_ocr_service
from services.api.src.ocr.schemas import OCRJobCreate, OCRJobResponse
from services.api.src.ocr.service import OCRService

router = APIRouter(prefix="/organizations/{org_id}/ocr/jobs", tags=["ocr-processing"])


@router.post(
    "",
    response_model=OCRJobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ocr_job(
    org_id: uuid.UUID,
    data: OCRJobCreate,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ocr_service: OCRService = Depends(get_ocr_service),  # noqa: B008
) -> Any:
    """Create a new OCR job for a document under an organization."""
    return await ocr_service.create_job(
        org_id=org_id,
        user_id=current_user.id,
        data=data,
    )


@router.get("/{job_id}", response_model=OCRJobResponse)
async def get_ocr_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ocr_service: OCRService = Depends(get_ocr_service),  # noqa: B008
) -> Any:
    """Retrieve details for a specific OCR job."""
    return await ocr_service.get_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


@router.get("", response_model=list[OCRJobResponse])
async def list_ocr_jobs(
    org_id: uuid.UUID,
    status: str | None = Query(
        None, description="Filter by status (e.g. PENDING, RUNNING)"
    ),  # noqa: B008
    engine: str | None = Query(
        None, description="Filter by engine (e.g. PADDLEOCR, TESSERACT)"
    ),  # noqa: B008
    skip: int = Query(0, ge=0),  # noqa: B008
    limit: int = Query(100, ge=1, le=100),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    ocr_service: OCRService = Depends(get_ocr_service),  # noqa: B008
) -> Any:
    """List OCR jobs under the organization workspace."""
    return await ocr_service.list_jobs(
        org_id=org_id,
        user_id=current_user.id,
        status=status,
        engine=engine,
        skip=skip,
        limit=limit,
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ocr_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ocr_service: OCRService = Depends(get_ocr_service),  # noqa: B008
) -> None:
    """Permanently delete an OCR job and its results."""
    await ocr_service.delete_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


@router.post("/{job_id}/cancel", response_model=OCRJobResponse)
async def cancel_ocr_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ocr_service: OCRService = Depends(get_ocr_service),  # noqa: B008
) -> Any:
    """Cancel an active, queued, or pending OCR job."""
    return await ocr_service.cancel_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


@router.post("/{job_id}/retry", response_model=OCRJobResponse)
async def retry_ocr_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ocr_service: OCRService = Depends(get_ocr_service),  # noqa: B008
) -> Any:
    """Retry a failed or cancelled OCR job."""
    return await ocr_service.retry_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )
