import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IConnector(ABC):
    """Interface executing auth operations and data uploads on targets."""

    @abstractmethod
    async def authenticate(self, credentials: dict[str, Any]) -> bool:
        """Evaluate credential token parameters validity."""
        pass

    @abstractmethod
    async def push_data(
        self, data: Sequence[dict[str, Any]], target_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Push batch row payload arrays directly into targets."""
        pass


class ISyncEngine(ABC):
    """Interface coordinating sync queues, discovery, and dispatches."""

    @abstractmethod
    async def register_connector(
        self, name: str, connector_type: str
    ) -> uuid.UUID:
        """Register a new connector capability in the system."""
        pass

    @abstractmethod
    async def execute_job(self, job_id: uuid.UUID) -> dict[str, Any]:
        """Load job properties, format mapped fields, and invoke target pushes."""
        pass

    @abstractmethod
    async def dispatch_retry_queue(self) -> int:
        """Scan dead letter queues and invoke automatic retry strategies."""
        pass


class IConnectorFactory(ABC):
    """Interface fabricating integration connector wrappers."""

    @abstractmethod
    async def get_connector(self, connector_type: str) -> IConnector:
        """Instantiate wrapper instance based on targets."""
        pass
