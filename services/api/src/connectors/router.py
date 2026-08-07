# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.connectors.dependencies import (
    get_connector_studio_service,
)
from services.api.src.connectors.schemas import (
    ConnectorAccountCreate,
    ConnectorAccountResponse,
    ConnectorConnectionCreate,
    ConnectorConnectionResponse,
    ConnectorConnectionUpdate,
    ConnectorCreate,
    ConnectorResponse,
)
from services.api.src.connectors.service import ConnectorStudioService

router = APIRouter(prefix="/connectors-studio", tags=["connectors_studio"])


# ----------------------------------------------------
# Driver Registry Endpoints
# ----------------------------------------------------

@router.post(
    "/drivers/install",
    response_model=ConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def install_connector_driver(
    payload: ConnectorCreate,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Install a new connector driver metadata."""
    conn_id = await service.install_connector(
        payload.name, payload.connector_type
    )
    return await service.studio_repo.get_connector_by_id(conn_id)


@router.get("/drivers", response_model=list[ConnectorResponse])
async def list_installed_drivers(
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """List drivers installed in the studio registry."""
    return await service.studio_repo.list_connectors()


# ----------------------------------------------------
# Integrated Accounts Endpoints
# ----------------------------------------------------

@router.post(
    "/accounts",
    response_model=ConnectorAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_integrated_account(
    payload: ConnectorAccountCreate,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Create integrated external account profile."""
    return await service.create_account(
        connector_id=payload.connector_id,
        user_id=current_user.id,
        email=payload.account_email,
        label=payload.account_label,
        org_id=payload.organization_id,
    )


@router.get("/accounts", response_model=list[ConnectorAccountResponse])
async def list_integrated_accounts(
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """List accounts integrated in the connection manager."""
    return await service.connection_repo.list_accounts()


# ----------------------------------------------------
# Active Connection Links Endpoints
# ----------------------------------------------------

@router.post(
    "/connections",
    response_model=ConnectorConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_connection_bridge(
    payload: ConnectorConnectionCreate,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Create a new active connection bridge link."""
    # Encrypt credentials prior to saving
    enc_token = await service.encrypt_credential(payload.plain_token)

    conn_id = await service.create_connection(
        account_id=payload.account_id, name=payload.name
    )

    # Save credentials linked to connection
    from services.api.src.connectors.models import ConnectorCredential

    db_cred = ConnectorCredential(
        connection_id=conn_id,
        encrypted_token=enc_token,
    )
    service.connection_repo.session.add(db_cred)
    await service.connection_repo.session.flush()

    return await service.get_connection(conn_id)


@router.get("/connections", response_model=list[ConnectorConnectionResponse])
async def list_configured_connections(
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """List configured connection bridges."""
    return await service.list_active_connections()


@router.get(
    "/connections/{connection_id}",
    response_model=ConnectorConnectionResponse,
)
async def get_connection_details(
    connection_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Retrieve detailed properties of a configured connection link."""
    return await service.get_connection(connection_id)


@router.patch(
    "/connections/{connection_id}",
    response_model=ConnectorConnectionResponse,
)
async def update_connection_properties(
    connection_id: uuid.UUID,
    payload: ConnectorConnectionUpdate,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Update configured properties of a connection link."""
    return await service.update_connection(
        connection_id=connection_id, labels=payload.labels, tags=payload.tags
    )


@router.delete(
    "/connections/{connection_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_connection_bridge(
    connection_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> None:
    """Delete configured connections from the database."""
    await service.delete_connection(connection_id)


# ----------------------------------------------------
# Health & Operations Endpoints
# ----------------------------------------------------

@router.post("/connections/{connection_id}/test")
async def test_connection_ping(
    connection_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Run standard connection handshake test."""
    success = await service.test_connection(connection_id)
    return {"success": success}


@router.post("/connections/{connection_id}/refresh")
async def refresh_connection_tokens(
    connection_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Trigger credentials tokens refresh routine."""
    success = await service.refresh_connection(connection_id)
    return {"success": success}


@router.post("/connections/{connection_id}/health")
async def check_connection_health(
    connection_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ConnectorStudioService = Depends(get_connector_studio_service),
) -> Any:
    """Run live health check audit on configured connection."""
    health_status = await service.check_health(connection_id)
    return {"health_status": health_status}
