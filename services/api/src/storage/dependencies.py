# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.storage.repository import (
    StorageFileRepository,
    StorageProviderRepository,
    StorageQuotaRepository,
)
from services.api.src.storage.service import StorageService


def get_storage_provider_repository(
    session: AsyncSession = Depends(get_db),
) -> StorageProviderRepository:
    """Inject StorageProviderRepository context."""
    return StorageProviderRepository(session)


def get_storage_file_repository(
    session: AsyncSession = Depends(get_db),
) -> StorageFileRepository:
    """Inject StorageFileRepository context."""
    return StorageFileRepository(session)


def get_storage_quota_repository(
    session: AsyncSession = Depends(get_db),
) -> StorageQuotaRepository:
    """Inject StorageQuotaRepository context."""
    return StorageQuotaRepository(session)


def get_storage_service(
    provider_repo: StorageProviderRepository = Depends(get_storage_provider_repository),
    file_repo: StorageFileRepository = Depends(get_storage_file_repository),
    quota_repo: StorageQuotaRepository = Depends(get_storage_quota_repository),
) -> StorageService:
    """Inject StorageService context."""
    return StorageService(provider_repo, file_repo, quota_repo)
