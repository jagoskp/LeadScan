# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.ai_understanding.repository import (
    DetectedEntityRepository,
    UnderstandingJobRepository,
)
from services.api.src.ai_understanding.service import AIUnderstandingService
from services.api.src.database import get_db


def get_understanding_job_repository(
    session: AsyncSession = Depends(get_db),
) -> UnderstandingJobRepository:
    """Inject UnderstandingJobRepository context."""
    return UnderstandingJobRepository(session)


def get_detected_entity_repository(
    session: AsyncSession = Depends(get_db),
) -> DetectedEntityRepository:
    """Inject DetectedEntityRepository context."""
    return DetectedEntityRepository(session)


def get_ai_understanding_service(
    job_repo: UnderstandingJobRepository = Depends(
        get_understanding_job_repository
    ),
    entity_repo: DetectedEntityRepository = Depends(
        get_detected_entity_repository
    ),
) -> AIUnderstandingService:
    """Inject AIUnderstandingService context."""
    return AIUnderstandingService(job_repo, entity_repo)
