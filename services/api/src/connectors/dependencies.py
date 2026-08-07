# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.connectors.repository import (
    ConnectorConnectionRepository,
    ConnectorStudioRepository,
)
from services.api.src.connectors.service import ConnectorStudioService
from services.api.src.database import get_db


def get_connector_studio_repository(
    session: AsyncSession = Depends(get_db),
) -> ConnectorStudioRepository:
    """Inject ConnectorStudioRepository context."""
    return ConnectorStudioRepository(session)


def get_connector_connection_repository(
    session: AsyncSession = Depends(get_db),
) -> ConnectorConnectionRepository:
    """Inject ConnectorConnectionRepository context."""
    return ConnectorConnectionRepository(session)


def get_connector_studio_service(
    studio_repo: ConnectorStudioRepository = Depends(
        get_connector_studio_repository
    ),
    connection_repo: ConnectorConnectionRepository = Depends(
        get_connector_connection_repository
    ),
) -> ConnectorStudioService:
    """Inject ConnectorStudioService context."""
    return ConnectorStudioService(studio_repo, connection_repo)
