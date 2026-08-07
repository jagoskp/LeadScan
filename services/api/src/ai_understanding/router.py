# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.ai_understanding.dependencies import (
    get_ai_understanding_service,
)
from services.api.src.ai_understanding.exceptions import EntityNotFoundException
from services.api.src.ai_understanding.schemas import (
    DetectedEntityResponse,
    UnderstandingJobCreate,
    UnderstandingJobResponse,
)
from services.api.src.ai_understanding.service import AIUnderstandingService
from services.api.src.ai_understanding.validators import (
    validate_document_type,
)
from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User

router = APIRouter(prefix="/ai-understanding", tags=["ai_understanding"])


# ----------------------------------------------------
# AI Understanding Jobs Endpoints
# ----------------------------------------------------

@router.post(
    "/jobs",
    response_model=UnderstandingJobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_understanding_job(
    data: UnderstandingJobCreate,
    current_user: User = Depends(get_current_user),
    service: AIUnderstandingService = Depends(get_ai_understanding_service),
) -> Any:
    """Create a new AI understanding job and run the mock pipeline flow."""
    validate_document_type(data.document_type.value)

    # Register/create job
    job = await service.create_job(user_id=current_user.id, data=data)
    # Execute structural mock pipeline immediately to populate results
    return await service.execute_understanding(job.id)


@router.get("/jobs", response_model=list[UnderstandingJobResponse])
async def list_understanding_jobs(
    organization_id: uuid.UUID | None = Query(
        None, description="Filter by organization"
    ),
    current_user: User = Depends(get_current_user),
    service: AIUnderstandingService = Depends(get_ai_understanding_service),
) -> Any:
    """List AI jobs filtered by user context and organization."""
    return await service.list_jobs(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/jobs/{job_id}", response_model=UnderstandingJobResponse)
async def get_understanding_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: AIUnderstandingService = Depends(get_ai_understanding_service),
) -> Any:
    """Retrieve detailed properties of a single AI understanding job."""
    return await service.get_job(job_id)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_understanding_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: AIUnderstandingService = Depends(get_ai_understanding_service),
) -> None:
    """Cancel and delete an AI job configuration."""
    await service.delete_job(job_id)


# ----------------------------------------------------
# AI Entities Endpoints
# ----------------------------------------------------

@router.get("/entities/{entity_id}", response_model=DetectedEntityResponse)
async def get_detected_entity(
    entity_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: AIUnderstandingService = Depends(get_ai_understanding_service),
) -> Any:
    """Retrieve detailed properties of an individual detected entity."""
    entity = await service.entity_repo.get_entity_by_id(entity_id)
    if not entity:
        raise EntityNotFoundException()
    return entity
