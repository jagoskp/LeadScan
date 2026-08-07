import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.connectors.models import (
    Connector,
    ConnectorAccount,
    ConnectorAudit,
    ConnectorConnection,
    ConnectorHealth,
    ConnectorPermission,
)


class ConnectorStudioRepository:
    """Repository handling persistence operations for core connector registrations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_connector(self, connector: Connector) -> Connector:
        """Persist a core Connector registration driver."""
        self.session.add(connector)
        await self.session.flush()
        return connector

    async def get_connector_by_id(
        self, connector_id: uuid.UUID
    ) -> Connector | None:
        """Retrieve Connector registry preloading accounts."""
        stmt = (
            select(Connector)
            .where(Connector.id == connector_id)
            .options(selectinload(Connector.accounts))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_connectors(self) -> Sequence[Connector]:
        """List registered connectors."""
        stmt = select(Connector)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_connector_status(
        self, connector_id: uuid.UUID, is_active: bool
    ) -> Connector | None:
        """Enable or disable connector drivers."""
        stmt = (
            update(Connector)
            .where(Connector.id == connector_id)
            .values(is_active=is_active)
        )
        await self.session.execute(stmt)
        return await self.get_connector_by_id(connector_id)


class ConnectorConnectionRepository:
    """Repository handling connection links, credentials, healths, and audits."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_account(
        self, account: ConnectorAccount
    ) -> ConnectorAccount:
        """Persist ConnectorAccount details."""
        self.session.add(account)
        await self.session.flush()
        return account

    async def get_account_by_id(
        self, account_id: uuid.UUID
    ) -> ConnectorAccount | None:
        """Retrieve ConnectorAccount preloading connections."""
        stmt = (
            select(ConnectorAccount)
            .where(ConnectorAccount.id == account_id)
            .options(selectinload(ConnectorAccount.connections))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_accounts(self) -> Sequence[ConnectorAccount]:
        """List integrated user accounts."""
        stmt = select(ConnectorAccount)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_connection(
        self, connection: ConnectorConnection
    ) -> ConnectorConnection:
        """Persist ConnectorConnection configurations."""
        self.session.add(connection)
        await self.session.flush()
        return connection

    async def get_connection_by_id(
        self, connection_id: uuid.UUID
    ) -> ConnectorConnection | None:
        """Retrieve ConnectorConnection preloading status lists and keys."""
        stmt = (
            select(ConnectorConnection)
            .where(ConnectorConnection.id == connection_id)
            .options(
                selectinload(ConnectorConnection.credentials),
                selectinload(ConnectorConnection.health_records),
                selectinload(ConnectorConnection.audit_logs),
                selectinload(ConnectorConnection.permissions),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_connections(self) -> Sequence[ConnectorConnection]:
        """List configured connections bridges."""
        stmt = select(ConnectorConnection).options(
            selectinload(ConnectorConnection.health_records),
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_connection_properties(
        self, connection_id: uuid.UUID, data: dict[str, Any]
    ) -> ConnectorConnection | None:
        """Update connection parameters or enabled statuses."""
        if data:
            stmt = (
                update(ConnectorConnection)
                .where(ConnectorConnection.id == connection_id)
                .values(**data)
            )
            await self.session.execute(stmt)
        return await self.get_connection_by_id(connection_id)

    async def delete_connection(self, connection_id: uuid.UUID) -> bool:
        """Delete configured connections from the database."""
        stmt = delete(ConnectorConnection).where(
            ConnectorConnection.id == connection_id
        )
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))

    async def create_health(self, health: ConnectorHealth) -> ConnectorHealth:
        """Persist health check records."""
        self.session.add(health)
        await self.session.flush()
        return health

    async def create_audit(self, audit: ConnectorAudit) -> ConnectorAudit:
        """Persist security audit trail logs."""
        self.session.add(audit)
        await self.session.flush()
        return audit

    async def create_permission(
        self, permission: ConnectorPermission
    ) -> ConnectorPermission:
        """Persist user access permission controls."""
        self.session.add(permission)
        await self.session.flush()
        return permission
