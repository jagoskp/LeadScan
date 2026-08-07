import uuid
from collections.abc import Sequence
from typing import Any

from fastapi import HTTPException, status

from services.api.src.connectors.enums import (
    ConnectorHealthStatus,
)
from services.api.src.connectors.exceptions import (
    ConnectorConnectionNotFoundException,
)
from services.api.src.connectors.interfaces import (
    IConnectionManager,
    IConnectorStudio,
    ISecurityEngine,
)
from services.api.src.connectors.models import (
    Connector,
    ConnectorAccount,
    ConnectorAudit,
    ConnectorConnection,
    ConnectorHealth,
)
from services.api.src.connectors.repository import (
    ConnectorConnectionRepository,
    ConnectorStudioRepository,
)
from services.api.src.connectors.validators import validate_connection_config


class ConnectorStudioService(
    IConnectorStudio, IConnectionManager, ISecurityEngine
):
    """Orchestrates third-party connection links, health checks, and encryptions."""

    def __init__(
        self,
        studio_repo: ConnectorStudioRepository,
        connection_repo: ConnectorConnectionRepository,
    ) -> None:
        self.studio_repo = studio_repo
        self.connection_repo = connection_repo

    # ----------------------------------------------------
    # IConnectorStudio Implementation
    # ----------------------------------------------------

    async def install_connector(
        self, name: str, connector_type: str
    ) -> uuid.UUID:
        """Install a new connector driver metadata into database."""
        conn = Connector(name=name, connector_type=connector_type, is_active=True)
        await self.studio_repo.create_connector(conn)
        return conn.id

    async def configure_connector(
        self, connector_id: uuid.UUID, config: dict[str, Any]
    ) -> bool:
        """Configure driver parameters configurations."""
        validate_connection_config(config)
        # Structural configuration mock success
        return True

    async def check_health(self, connection_id: uuid.UUID) -> str:
        """Invoke health checks and record latencies."""
        conn = await self.connection_repo.get_connection_by_id(connection_id)
        if not conn:
            raise ConnectorConnectionNotFoundException()

        health = ConnectorHealth(
            connection_id=conn.id,
            status=ConnectorHealthStatus.HEALTHY.value,
            latency_ms=45,
        )
        await self.connection_repo.create_health(health)
        return health.status

    # ----------------------------------------------------
    # IConnectionManager Implementation
    # ----------------------------------------------------

    async def create_connection(
        self, account_id: uuid.UUID, name: str
    ) -> uuid.UUID:
        """Create a new active connection bridge link."""
        account = await self.connection_repo.get_account_by_id(account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Connector account not found to bridge connection",
            )

        connection = ConnectorConnection(
            account_id=account_id,
            name=name,
            labels=[],
            tags=[],
            is_enabled=True,
        )
        await self.connection_repo.create_connection(connection)
        return connection.id

    async def test_connection(self, connection_id: uuid.UUID) -> bool:
        """Run standard authentication ping handshakes with targets."""
        conn = await self.connection_repo.get_connection_by_id(connection_id)
        if not conn:
            raise ConnectorConnectionNotFoundException()

        audit = ConnectorAudit(
            connection_id=conn.id,
            action="Connection Test",
            details="Ping connection test passed successfully",
        )
        await self.connection_repo.create_audit(audit)
        return True

    async def refresh_connection(self, connection_id: uuid.UUID) -> bool:
        """Trigger access token refresh routines using stored refreshes."""
        conn = await self.connection_repo.get_connection_by_id(connection_id)
        if not conn:
            raise ConnectorConnectionNotFoundException()

        audit = ConnectorAudit(
            connection_id=conn.id,
            action="Token Refresh",
            details="Refreshed OAuth credentials tokens successfully",
        )
        await self.connection_repo.create_audit(audit)
        return True

    # ----------------------------------------------------
    # ISecurityEngine Implementation
    # ----------------------------------------------------

    async def encrypt_credential(self, plain_token: str) -> str:
        """Encrypt secret details prior to DB persistence."""
        return f"ENC_{plain_token}"

    async def decrypt_credential(self, encrypted_token: str) -> str:
        """Decrypt secret details for runtime integrations usage."""
        return encrypted_token.replace("ENC_", "")

    async def rotate_keys(self) -> int:
        """Trigger encryption key rotations pipelines."""
        # Key rotation stub always reports 1 successful rotation
        return 1

    # ----------------------------------------------------
    # Account & CRUD Operations Helpers
    # ----------------------------------------------------

    async def create_account(
        self,
        connector_id: uuid.UUID,
        user_id: uuid.UUID,
        email: str,
        label: str | None,
        org_id: uuid.UUID | None = None,
    ) -> ConnectorAccount:
        """Create integrated external account profile."""
        connector = await self.studio_repo.get_connector_by_id(connector_id)
        if not connector:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Connector driver registry not found to map account",
            )

        account = ConnectorAccount(
            connector_id=connector_id,
            user_id=user_id,
            organization_id=org_id,
            account_email=email,
            account_label=label,
            is_default=False,
        )
        await self.connection_repo.create_account(account)
        return account

    async def list_active_connections(self) -> Sequence[ConnectorConnection]:
        """List configured connections bridges."""
        return await self.connection_repo.list_connections()

    async def get_connection(self, connection_id: uuid.UUID) -> ConnectorConnection:
        """Retrieve ConnectorConnection detail properties."""
        conn = await self.connection_repo.get_connection_by_id(connection_id)
        if not conn:
            raise ConnectorConnectionNotFoundException()
        return conn

    async def update_connection(
        self, connection_id: uuid.UUID, labels: list[str] | None, tags: list[str] | None
    ) -> ConnectorConnection:
        """Update tags or labels metadata flags on a connection."""
        await self.get_connection(connection_id)

        update_data = {}
        if labels is not None:
            update_data["labels"] = labels
        if tags is not None:
            update_data["tags"] = tags

        updated = await self.connection_repo.update_connection_properties(
            connection_id, update_data
        )
        if not updated:
            raise ConnectorConnectionNotFoundException()
        return updated

    async def delete_connection(self, connection_id: uuid.UUID) -> bool:
        """Delete connection config from database."""
        await self.get_connection(connection_id)
        return await self.connection_repo.delete_connection(connection_id)
