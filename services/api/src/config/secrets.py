import os
from abc import ABC, abstractmethod


class ISecretManager(ABC):
    """Interface contract that all Secret Managers must implement."""

    @abstractmethod
    def get_secret(self, key: str, default: str | None = None) -> str | None:
        """Resolve the secret value associated with the given key name."""
        pass


class EnvSecretManager(ISecretManager):
    """Local Secret Manager resolving values from local environment variables."""

    def get_secret(self, key: str, default: str | None = None) -> str | None:
        """Fetch secret from environment scope."""
        return os.environ.get(key, default)
