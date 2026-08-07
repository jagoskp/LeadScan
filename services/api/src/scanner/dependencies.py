# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.scanner.repository import ScanJobRepository, ScanResultRepository
from services.api.src.scanner.service import ScannerService


def get_scan_job_repository(
    session: AsyncSession = Depends(get_db),
) -> ScanJobRepository:
    """Inject ScanJobRepository context."""
    return ScanJobRepository(session)


def get_scan_result_repository(
    session: AsyncSession = Depends(get_db),
) -> ScanResultRepository:
    """Inject ScanResultRepository context."""
    return ScanResultRepository(session)


def get_scanner_service(
    job_repo: ScanJobRepository = Depends(get_scan_job_repository),
    result_repo: ScanResultRepository = Depends(get_scan_result_repository),
) -> ScannerService:
    """Inject ScannerService context."""
    return ScannerService(job_repo, result_repo)
