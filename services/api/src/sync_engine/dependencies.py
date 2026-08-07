# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.sync_engine.repository import (
    ConnectorRepository,
    SyncJobRepository,
)
from services.api.src.sync_engine.service import SyncEngineService


def get_connector_repository(
    session: AsyncSession = Depends(get_db),
) -> ConnectorRepository:
    """Inject ConnectorRepository context."""
    return ConnectorRepository(session)


def get_sync_job_repository(
    session: AsyncSession = Depends(get_db),
) -> SyncJobRepository:
    """Inject SyncJobRepository context."""
    return SyncJobRepository(session)


def get_sync_engine_service(
    connector_repo: ConnectorRepository = Depends(get_connector_repository),
    job_repo: SyncJobRepository = Depends(get_sync_job_repository),
) -> SyncEngineService:
    """Inject SyncEngineService context."""
    return SyncEngineService(connector_repo, job_repo)
