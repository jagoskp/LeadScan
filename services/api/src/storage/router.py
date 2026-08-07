# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.storage.dependencies import get_storage_service
from services.api.src.storage.schemas import (
    StorageFileCreate,
    StorageFileResponse,
    StorageFileStatus,
    StorageFileUpdate,
    StorageProviderCreate,
    StorageProviderResponse,
    StorageProviderUpdate,
    StorageQuotaResponse,
    StorageQuotaUpdate,
)
from services.api.src.storage.service import StorageService

router = APIRouter(prefix="/storage", tags=["storage"])


# ----------------------------------------------------
# Storage Providers Endpoints
# ----------------------------------------------------


@router.post(
    "/providers",
    response_model=StorageProviderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_provider(
    data: StorageProviderCreate,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Register a new storage provider configuration context."""
    return await service.register_provider(current_user, data)


@router.get("/providers", response_model=list[StorageProviderResponse])
async def list_providers(
    organization_id: uuid.UUID | None = Query(
        None, description="Filter by organization"
    ),
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """List active storage providers configured for the user scope."""
    return await service.list_providers(current_user, organization_id)


@router.get("/providers/{provider_id}", response_model=StorageProviderResponse)
async def get_provider(
    provider_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Retrieve detailed configuration details of a single storage provider."""
    return await service.get_provider(provider_id, current_user)


@router.patch("/providers/{provider_id}", response_model=StorageProviderResponse)
async def update_provider(
    provider_id: uuid.UUID,
    data: StorageProviderUpdate,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Update configs of an existing storage provider."""
    return await service.update_provider(provider_id, current_user, data)


@router.patch("/providers/{provider_id}/health", response_model=StorageProviderResponse)
async def trigger_health_check(
    provider_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Simulate and register storage health checks."""
    return await service.check_health(provider_id, current_user)


@router.delete("/providers/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_provider(
    provider_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> None:
    """Delete storage provider configuration."""
    await service.delete_provider(provider_id, current_user)


# ----------------------------------------------------
# Storage Files Endpoints
# ----------------------------------------------------


@router.post(
    "/files", response_model=StorageFileResponse, status_code=status.HTTP_201_CREATED
)
async def register_file(
    data: StorageFileCreate,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Register file metadata, deducting allocated quota bytes."""
    return await service.register_file(current_user, data)


@router.get("/files/{file_id}", response_model=StorageFileResponse)
async def get_file_metadata(
    file_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Retrieve a specific file metadata record."""
    return await service.get_file(file_id, current_user)


@router.get("/files", response_model=list[StorageFileResponse])
async def list_files_metadata(
    organization_id: uuid.UUID = Query(..., description="Organization scope"),
    status: StorageFileStatus | None = Query(
        None, description="Filter by status (e.g. ACTIVE, SOFT_DELETED)"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """List file metadata records registered within an organization context."""
    status_str = status.value if status else None
    items, _ = await service.list_files(
        user=current_user,
        organization_id=organization_id,
        status=status_str,
        skip=skip,
        limit=limit,
    )
    return [StorageFileResponse.model_validate(item) for item in items]


@router.patch("/files/{file_id}", response_model=StorageFileResponse)
async def update_file_metadata(
    file_id: uuid.UUID,
    data: StorageFileUpdate,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Update metadata logs on an existing file registry."""
    return await service.update_file_metadata(file_id, current_user, data)


@router.patch("/files/{file_id}/soft-delete", response_model=StorageFileResponse)
async def soft_delete_file(
    file_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Mark a file as soft-deleted, releasing quota consumption allocation."""
    return await service.soft_delete_file(file_id, current_user)


@router.patch("/files/{file_id}/restore", response_model=StorageFileResponse)
async def restore_file(
    file_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Restore a soft-deleted file, re-verifying and claiming quota usage."""
    return await service.restore_file(file_id, current_user)


@router.patch("/files/{file_id}/cleanup", response_model=StorageFileResponse)
async def cleanup_file(
    file_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Clean metadata logs, declaring final cleanup state."""
    return await service.cleanup_file(file_id, current_user)


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_metadata(
    file_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> None:
    """Hard delete metadata logs from DB."""
    await service.delete_file_metadata(file_id, current_user)


# ----------------------------------------------------
# Storage Quotas Endpoints
# ----------------------------------------------------


@router.get("/quota", response_model=StorageQuotaResponse)
async def get_storage_quota(
    organization_id: uuid.UUID = Query(..., description="Organization scope"),
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Retrieve quota profile context and current usage statistics."""
    return await service.get_quota(current_user, organization_id)


@router.patch("/quota", response_model=StorageQuotaResponse)
async def update_storage_quota(
    data: StorageQuotaUpdate,
    organization_id: uuid.UUID = Query(..., description="Organization scope"),
    current_user: User = Depends(get_current_user),
    service: StorageService = Depends(get_storage_service),
) -> Any:
    """Modify maximum bytes allocation limit for an organization (admin only)."""
    return await service.update_quota_limit(
        current_user, organization_id, data.max_bytes
    )
