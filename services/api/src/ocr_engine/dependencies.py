# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.ocr_engine.repository import (
    OCRJobRepository,
    OCRPageRepository,
)
from services.api.src.ocr_engine.service import OCREngineService


def get_ocr_job_repository(
    session: AsyncSession = Depends(get_db),
) -> OCRJobRepository:
    """Inject OCRJobRepository context."""
    return OCRJobRepository(session)


def get_ocr_page_repository(
    session: AsyncSession = Depends(get_db),
) -> OCRPageRepository:
    """Inject OCRPageRepository context."""
    return OCRPageRepository(session)


def get_ocr_engine_service(
    job_repo: OCRJobRepository = Depends(get_ocr_job_repository),
    page_repo: OCRPageRepository = Depends(get_ocr_page_repository),
) -> OCREngineService:
    """Inject OCREngineService context."""
    return OCREngineService(job_repo, page_repo)
