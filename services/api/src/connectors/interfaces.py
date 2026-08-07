import uuid
from abc import ABC, abstractmethod
from typing import Any


class IConnectorStudio(ABC):
    """Interface executing connector installs, discovery, and health audits."""

    @abstractmethod
    async def install_connector(self, name: str, connector_type: str) -> uuid.UUID:
        """Install a new connector driver metadata into database."""
        pass

    @abstractmethod
    async def configure_connector(
        self, connector_id: uuid.UUID, config: dict[str, Any]
    ) -> bool:
        """Database model storing registered connectors
        configurations (e.g. Google Sheets).
        """
        pass

    @abstractmethod
    async def check_health(self, connection_id: uuid.UUID) -> str:
        """Invoke health checks and record latencies."""
        pass


class IConnectionManager(ABC):
    """Interface orchestrating user account connections
    creation, validation, and refreshes.
    """

    @abstractmethod
    async def create_connection(self, account_id: uuid.UUID, name: str) -> uuid.UUID:
        """Create a new active connection bridge link."""
        pass

    @abstractmethod
    async def test_connection(self, connection_id: uuid.UUID) -> bool:
        """Run standard authentication ping handshakes with targets."""
        pass

    @abstractmethod
    async def refresh_connection(self, connection_id: uuid.UUID) -> bool:
        """Trigger access token refresh routines using stored refreshes."""
        pass


class ISecurityEngine(ABC):
    """Interface declaring credentials encryption bounds and rotations."""

    @abstractmethod
    async def encrypt_credential(self, plain_token: str) -> str:
        """Encrypt secret details prior to DB persistence."""
        pass

    @abstractmethod
    async def decrypt_credential(self, encrypted_token: str) -> str:
        """Decrypt secret details for runtime integrations usage."""
        pass

    @abstractmethod
    async def rotate_keys(self) -> int:
        """Trigger encryption key rotations pipelines."""
        pass
