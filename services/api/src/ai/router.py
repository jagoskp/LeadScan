import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.ai.dependencies import get_ai_service
from services.api.src.ai.schemas import AIJobCreate, AIJobResponse
from services.api.src.ai.service import AIService
from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User

router = APIRouter(prefix="/organizations/{org_id}/ai/jobs", tags=["ai-analysis"])


@router.post(
    "",
    response_model=AIJobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ai_job(
    org_id: uuid.UUID,
    data: AIJobCreate,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ai_service: AIService = Depends(get_ai_service),  # noqa: B008
) -> Any:
    """Create a new AI analysis job for a document under an organization."""
    return await ai_service.create_job(
        org_id=org_id,
        user_id=current_user.id,
        data=data,
    )


@router.get("/{job_id}", response_model=AIJobResponse)
async def get_ai_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ai_service: AIService = Depends(get_ai_service),  # noqa: B008
) -> Any:
    """Retrieve details for a specific AI analysis job."""
    return await ai_service.get_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


@router.get("", response_model=list[AIJobResponse])
async def list_ai_jobs(
    org_id: uuid.UUID,
    status: str | None = Query(
        None, description="Filter by status (e.g. PENDING, RUNNING)"
    ),  # noqa: B008
    provider: str | None = Query(
        None, description="Filter by provider (e.g. OPENAI, GEMINI, CLAUDE)"
    ),  # noqa: B008
    skip: int = Query(0, ge=0),  # noqa: B008
    limit: int = Query(100, ge=1, le=100),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    ai_service: AIService = Depends(get_ai_service),  # noqa: B008
) -> Any:
    """List AI analysis jobs under the organization workspace."""
    return await ai_service.list_jobs(
        org_id=org_id,
        user_id=current_user.id,
        status=status,
        provider=provider,
        skip=skip,
        limit=limit,
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ai_service: AIService = Depends(get_ai_service),  # noqa: B008
) -> None:
    """Permanently delete an AI analysis job and its results."""
    await ai_service.delete_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


@router.post("/{job_id}/cancel", response_model=AIJobResponse)
async def cancel_ai_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ai_service: AIService = Depends(get_ai_service),  # noqa: B008
) -> Any:
    """Cancel an active, queued, or pending AI analysis job."""
    return await ai_service.cancel_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )


@router.post("/{job_id}/retry", response_model=AIJobResponse)
async def retry_ai_job(
    org_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    ai_service: AIService = Depends(get_ai_service),  # noqa: B008
) -> Any:
    """Retry a failed or cancelled AI analysis job."""
    return await ai_service.retry_job(
        org_id=org_id,
        user_id=current_user.id,
        job_id=job_id,
    )
