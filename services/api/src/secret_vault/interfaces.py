import uuid
from abc import ABC, abstractmethod
from typing import Any


class ISecretVault(ABC):
    """Contract for core vault CRUD and lifecycle operations."""

    @abstractmethod
    async def create_secret(
        self,
        name: str,
        secret_type: str,
        plain_value: str,
        owner_id: uuid.UUID,
    ) -> uuid.UUID:
        """Encrypt and persist a new secret, returning its ID."""
        pass

    @abstractmethod
    async def retrieve_secret(
        self,
        secret_id: uuid.UUID,
        requester_id: uuid.UUID,
    ) -> str:
        """Validate access rights, decrypt and return the active secret value."""
        pass

    @abstractmethod
    async def rotate_secret(
        self,
        secret_id: uuid.UUID,
        new_plain_value: str,
        rotated_by: uuid.UUID,
    ) -> int:
        """Re-encrypt, snapshot the old version, and store the new version."""
        pass

    @abstractmethod
    async def archive_secret(
        self, secret_id: uuid.UUID, actor_id: uuid.UUID
    ) -> bool:
        """Mark secret as archived and write an audit entry."""
        pass

    @abstractmethod
    async def recover_secret(
        self, secret_id: uuid.UUID, actor_id: uuid.UUID
    ) -> bool:
        """Restore an archived secret to active status."""
        pass

    @abstractmethod
    async def delete_secret(
        self, secret_id: uuid.UUID, actor_id: uuid.UUID
    ) -> bool:
        """Permanently remove a secret and all its versions from the vault."""
        pass


class IEncryptionEngine(ABC):
    """Contract for symmetric encryption, envelope wrapping, and checksums."""

    @abstractmethod
    async def encrypt(self, plain_text: str) -> str:
        """Encrypt plain-text value using the active master key."""
        pass

    @abstractmethod
    async def decrypt(self, cipher_text: str) -> str:
        """Decrypt cipher-text using the matching key version."""
        pass

    @abstractmethod
    async def envelope_encrypt(
        self, plain_text: str, data_key: str
    ) -> dict[str, Any]:
        """Encrypt plain_text with data_key; wrap data_key with master key."""
        pass

    @abstractmethod
    async def checksum(self, value: str) -> str:
        """Compute an integrity checksum for the given value."""
        pass

    @abstractmethod
    async def verify_checksum(self, value: str, expected: str) -> bool:
        """Verify integrity by comparing computed checksum to expected."""
        pass


class IKeyManager(ABC):
    """Contract for master key retrieval, rotation scheduling, and HSM/KMS stubs."""

    @abstractmethod
    async def get_master_key(self) -> str:
        """Return the active master key reference (ID, not raw key material)."""
        pass

    @abstractmethod
    async def rotate_master_key(self) -> str:
        """Trigger a master key rotation and return the new key reference."""
        pass

    @abstractmethod
    async def schedule_rotation(
        self, secret_id: uuid.UUID, interval_days: int
    ) -> bool:
        """Register a rotation schedule for a given secret."""
        pass
