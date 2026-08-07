# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.sync_engine.dependencies import get_sync_engine_service
from services.api.src.sync_engine.schemas import (
    ConnectorCreate,
    ConnectorProfileCreate,
    ConnectorProfileResponse,
    ConnectorResponse,
    SyncJobCreate,
    SyncJobResponse,
)
from services.api.src.sync_engine.service import SyncEngineService

router = APIRouter(prefix="/sync", tags=["sync"])


# ----------------------------------------------------
# Connector Registry Endpoints
# ----------------------------------------------------

@router.post(
    "/connectors",
    response_model=ConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_connector(
    payload: ConnectorCreate,
    current_user: User = Depends(get_current_user),
    service: SyncEngineService = Depends(get_sync_engine_service),
) -> Any:
    """Register a new third-party integration connector."""
    conn_id = await service.register_connector(
        payload.name, payload.connector_type.value
    )
    conn = await service.connector_repo.get_connector_by_id(conn_id)
    return conn


@router.get("/connectors", response_model=list[ConnectorResponse])
async def list_connectors(
    current_user: User = Depends(get_current_user),
    service: SyncEngineService = Depends(get_sync_engine_service),
) -> Any:
    """List connectors registered in the database."""
    return await service.connector_repo.list_connectors()


# ----------------------------------------------------
# Connector Profiles Endpoints
# ----------------------------------------------------

@router.post(
    "/profiles",
    response_model=ConnectorProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_connector_profile(
    payload: ConnectorProfileCreate,
    current_user: User = Depends(get_current_user),
    service: SyncEngineService = Depends(get_sync_engine_service),
) -> Any:
    """Create a new connector configuration profile for an organization."""
    # Stub database setup for profile creation
    from services.api.src.sync_engine.models import (
        ConnectorCredential,
        ConnectorMetadata,
        ConnectorProfile,
    )

    profile = ConnectorProfile(
        connector_id=payload.connector_id,
        user_id=current_user.id,
        organization_id=payload.organization_id,
        name=payload.name,
        sync_mode=payload.sync_mode.value,
    )
    await service.connector_repo.create_profile(profile)

    for cred in payload.credentials:
        db_cred = ConnectorCredential(
            profile_id=profile.id,
            credential_type=cred.credential_type,
            encrypted_token=cred.encrypted_token,
            refresh_token=cred.refresh_token,
            expires_at=cred.expires_at,
        )
        service.connector_repo.session.add(db_cred)

    for meta in payload.metadata_records:
        db_meta = ConnectorMetadata(
            profile_id=profile.id,
            key=meta.key,
            value=meta.value,
        )
        service.connector_repo.session.add(db_meta)

    await service.connector_repo.session.flush()
    reloaded = await service.connector_repo.get_profile_by_id(profile.id)
    return reloaded


# ----------------------------------------------------
# Sync Job Queue Endpoints
# ----------------------------------------------------

@router.post(
    "/jobs",
    response_model=SyncJobResponse,
    status_code=status.HTTP_201_CREATED,
)
async def enqueue_sync_job(
    payload: SyncJobCreate,
    current_user: User = Depends(get_current_user),
    service: SyncEngineService = Depends(get_sync_engine_service),
) -> Any:
    """Add a new job in the synchronization queue."""
    return await service.create_job(payload)


@router.get("/jobs/{job_id}", response_model=SyncJobResponse)
async def get_sync_job_status(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SyncEngineService = Depends(get_sync_engine_service),
) -> Any:
    """Retrieve detailed properties of a SyncJob."""
    return await service.get_sync_job(job_id)


@router.post("/jobs/{job_id}/execute")
async def execute_sync_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SyncEngineService = Depends(get_sync_engine_service),
) -> Any:
    """Trigger synchronization job push actions."""
    return await service.execute_job(job_id)


@router.post("/retry")
async def process_retry_queue(
    current_user: User = Depends(get_current_user),
    service: SyncEngineService = Depends(get_sync_engine_service),
) -> Any:
    """Process retry attempts for failed queue jobs."""
    processed = await service.dispatch_retry_queue()
    return {"processed_retries_count": processed}
