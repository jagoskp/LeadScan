# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.ocr_engine.dependencies import get_ocr_engine_service
from services.api.src.ocr_engine.exceptions import OCRPageNotFoundException
from services.api.src.ocr_engine.schemas import (
    OCRJobCreate,
    OCRJobResponse,
    OCRPageResponse,
)
from services.api.src.ocr_engine.service import OCREngineService
from services.api.src.ocr_engine.validators import (
    validate_image_file,
    validate_ocr_languages,
)

router = APIRouter(prefix="/ocr", tags=["ocr"])


# ----------------------------------------------------
# OCR Jobs Endpoints
# ----------------------------------------------------

@router.post(
    "/jobs",
    response_model=OCRJobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ocr_job(
    data: OCRJobCreate,
    current_user: User = Depends(get_current_user),
    service: OCREngineService = Depends(get_ocr_engine_service),
) -> Any:
    """Create a new OCR job and execute the architectural mock pipeline."""
    validate_image_file(data.file_path)
    validate_ocr_languages(data.languages)

    # Register/create job
    job = await service.create_job(user_id=current_user.id, data=data)
    # Execute structural mock pipeline immediately to populate results
    return await service.execute_ocr(job.id)


@router.get("/jobs", response_model=list[OCRJobResponse])
async def list_ocr_jobs(
    organization_id: uuid.UUID | None = Query(
        None, description="Filter by organization"
    ),
    current_user: User = Depends(get_current_user),
    service: OCREngineService = Depends(get_ocr_engine_service),
) -> Any:
    """List OCR jobs filtered by user context and organization."""
    return await service.list_jobs(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/jobs/{job_id}", response_model=OCRJobResponse)
async def get_ocr_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: OCREngineService = Depends(get_ocr_engine_service),
) -> Any:
    """Retrieve detailed properties of a single OCR job."""
    return await service.get_job(job_id)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ocr_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: OCREngineService = Depends(get_ocr_engine_service),
) -> None:
    """Cancel and delete an OCR job configuration."""
    await service.delete_job(job_id)


# ----------------------------------------------------
# OCR Pages Endpoints
# ----------------------------------------------------

@router.get("/pages/{page_id}", response_model=OCRPageResponse)
async def get_ocr_page(
    page_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: OCREngineService = Depends(get_ocr_engine_service),
) -> Any:
    """Retrieve detailed layout structures of an individual page extract."""
    page = await service.page_repo.get_page_by_id(page_id)
    if not page:
        raise OCRPageNotFoundException()
    return page
