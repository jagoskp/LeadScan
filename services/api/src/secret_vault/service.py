import hashlib
import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from services.api.src.secret_vault.enums import (
    AuditAction,
    SecretStatus,
)
from services.api.src.secret_vault.exceptions import (
    SecretAccessDeniedException,
    SecretNotFoundException,
    SecretRotationFailedException,
)
from services.api.src.secret_vault.interfaces import (
    IEncryptionEngine,
    IKeyManager,
    ISecretVault,
)
from services.api.src.secret_vault.models import (
    Secret,
    SecretAccess,
    SecretAudit,
    SecretMetadata,
    SecretPolicy,
    SecretRotation,
    SecretVersion,
)
from services.api.src.secret_vault.repository import SecretRepository
from services.api.src.secret_vault.schemas import (
    SecretAccessCreate,
    SecretCreate,
    SecretMetadataCreate,
    SecretPolicyCreate,
)
from services.api.src.secret_vault.validators import (
    validate_policy_config,
    validate_secret_not_expired,
)


class SecretVaultService(ISecretVault, IEncryptionEngine, IKeyManager):
    """Orchestrates secret lifecycle, encryption stubs, and key management."""

    def __init__(self, repo: SecretRepository) -> None:
        self.repo = repo

    # ── ISecretVault ───────────────────────────────────

    async def create_secret(
        self,
        name: str,
        secret_type: str,
        plain_value: str,
        owner_id: uuid.UUID,
    ) -> uuid.UUID:
        """Encrypt and persist a new secret, returning its ID."""
        encrypted = await self.encrypt(plain_value)
        csum = await self.checksum(plain_value)

        secret = Secret(
            name=name,
            secret_type=secret_type,
            status=SecretStatus.ACTIVE.value,
            owner_id=owner_id,
        )
        await self.repo.create_secret(secret)

        version = SecretVersion(
            secret_id=secret.id,
            version_number=1,
            encrypted_value=encrypted,
            checksum=csum,
            key_reference=await self.get_master_key(),
            is_active=True,
        )
        await self.repo.create_version(version)

        audit = SecretAudit(
            secret_id=secret.id,
            actor_id=owner_id,
            action=AuditAction.CREATE.value,
            new_version=1,
            success=True,
        )
        await self.repo.create_audit(audit)

        return secret.id

    async def retrieve_secret(
        self,
        secret_id: uuid.UUID,
        requester_id: uuid.UUID,
    ) -> str:
        """Validate access, decrypt and return the active secret value."""
        secret = await self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundException()

        validate_secret_not_expired(secret.status, secret.expires_at)

        access = await self.repo.get_access_for_requester(
            secret_id, requester_id
        )
        is_owner = secret.owner_id == requester_id
        if not is_owner and not access:
            audit = SecretAudit(
                secret_id=secret_id,
                actor_id=requester_id,
                action=AuditAction.ACCESS_ATTEMPT.value,
                success=False,
            )
            await self.repo.create_audit(audit)
            raise SecretAccessDeniedException()

        active_ver = await self.repo.get_active_version(secret_id)
        if not active_ver:
            raise SecretNotFoundException()

        audit = SecretAudit(
            secret_id=secret_id,
            actor_id=requester_id,
            action=AuditAction.READ.value,
            success=True,
        )
        await self.repo.create_audit(audit)

        return await self.decrypt(active_ver.encrypted_value)

    async def rotate_secret(
        self,
        secret_id: uuid.UUID,
        new_plain_value: str,
        rotated_by: uuid.UUID,
    ) -> int:
        """Re-encrypt and version the secret, archiving the old version."""
        secret = await self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundException()

        try:
            old_ver = await self.repo.get_active_version(secret_id)
            old_version_number = old_ver.version_number if old_ver else 0

            await self.repo.deactivate_versions(secret_id)

            new_encrypted = await self.encrypt(new_plain_value)
            new_csum = await self.checksum(new_plain_value)
            new_version_number = old_version_number + 1

            new_ver = SecretVersion(
                secret_id=secret_id,
                version_number=new_version_number,
                encrypted_value=new_encrypted,
                checksum=new_csum,
                key_reference=await self.get_master_key(),
                is_active=True,
            )
            await self.repo.create_version(new_ver)

            rotation = SecretRotation(
                secret_id=secret_id,
                last_rotated_at=datetime.now(UTC),
                rotation_count=(
                    (secret.rotations[0].rotation_count + 1)
                    if secret.rotations
                    else 1
                ),
            )
            await self.repo.create_rotation(rotation)

            audit = SecretAudit(
                secret_id=secret_id,
                actor_id=rotated_by,
                action=AuditAction.ROTATE.value,
                old_version=old_version_number,
                new_version=new_version_number,
                success=True,
            )
            await self.repo.create_audit(audit)

        except Exception as exc:
            audit = SecretAudit(
                secret_id=secret_id,
                actor_id=rotated_by,
                action=AuditAction.ROTATION_FAILURE.value,
                success=False,
                reason=str(exc),
            )
            await self.repo.create_audit(audit)
            raise SecretRotationFailedException(str(exc)) from exc

        return new_version_number

    async def archive_secret(
        self, secret_id: uuid.UUID, actor_id: uuid.UUID
    ) -> bool:
        secret = await self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundException()
        await self.repo.update_status(secret_id, SecretStatus.ARCHIVED.value)
        await self.repo.create_audit(
            SecretAudit(
                secret_id=secret_id,
                actor_id=actor_id,
                action=AuditAction.ARCHIVE.value,
                success=True,
            )
        )
        return True

    async def recover_secret(
        self, secret_id: uuid.UUID, actor_id: uuid.UUID
    ) -> bool:
        secret = await self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundException()
        await self.repo.update_status(secret_id, SecretStatus.ACTIVE.value)
        await self.repo.create_audit(
            SecretAudit(
                secret_id=secret_id,
                actor_id=actor_id,
                action=AuditAction.RECOVER.value,
                success=True,
            )
        )
        return True

    async def delete_secret(
        self, secret_id: uuid.UUID, actor_id: uuid.UUID
    ) -> bool:
        secret = await self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundException()
        await self.repo.create_audit(
            SecretAudit(
                secret_id=secret_id,
                actor_id=actor_id,
                action=AuditAction.DELETE.value,
                success=True,
            )
        )
        return await self.repo.delete_secret(secret_id)

    # ── CRUD helpers ───────────────────────────────────

    async def create_from_schema(
        self, data: SecretCreate, owner_id: uuid.UUID
    ) -> Secret:
        sid = await self.create_secret(
            name=data.name,
            secret_type=data.secret_type.value,
            plain_value=data.plain_value,
            owner_id=owner_id,
        )
        secret = await self.repo.get_by_id(sid)
        if not secret:
            raise SecretNotFoundException()
        return secret

    async def list_secrets(self) -> Sequence[Secret]:
        return await self.repo.list_secrets()

    async def get_secret(self, secret_id: uuid.UUID) -> Secret:
        secret = await self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundException()
        return secret

    async def grant_access(
        self,
        secret_id: uuid.UUID,
        payload: SecretAccessCreate,
        actor_id: uuid.UUID,
    ) -> SecretAccess:
        await self.get_secret(secret_id)
        access = SecretAccess(
            secret_id=secret_id,
            grantee_user_id=payload.grantee_user_id,
            connector_id=payload.connector_id,
            role=payload.role.value,
        )
        await self.repo.create_access(access)
        await self.repo.create_audit(
            SecretAudit(
                secret_id=secret_id,
                actor_id=actor_id,
                action=AuditAction.UPDATE.value,
                success=True,
                reason="Access grant created",
            )
        )
        return access

    async def set_policy(
        self,
        secret_id: uuid.UUID,
        payload: SecretPolicyCreate,
    ) -> SecretPolicy:
        validate_policy_config(
            payload.rotation_interval_days, payload.max_versions
        )
        await self.get_secret(secret_id)
        policy = SecretPolicy(
            secret_id=secret_id,
            rotation_interval_days=payload.rotation_interval_days,
            max_versions=payload.max_versions,
            auto_rotate=payload.auto_rotate,
            expiry_days=payload.expiry_days,
        )
        return await self.repo.create_policy(policy)

    async def add_metadata(
        self,
        secret_id: uuid.UUID,
        payload: SecretMetadataCreate,
    ) -> SecretMetadata:
        await self.get_secret(secret_id)
        enc_val = await self.encrypt(payload.plain_value)
        meta = SecretMetadata(
            secret_id=secret_id,
            key=payload.key,
            encrypted_value=enc_val,
        )
        return await self.repo.create_metadata(meta)

    # ── IEncryptionEngine ──────────────────────────────

    async def encrypt(self, plain_text: str) -> str:
        """Stub: prefix simulates AES-256-GCM envelope encryption."""
        return f"ENC_V1::{plain_text}"

    async def decrypt(self, cipher_text: str) -> str:
        """Stub: strip encryption prefix to return plain value."""
        return cipher_text.replace("ENC_V1::", "")

    async def envelope_encrypt(
        self, plain_text: str, data_key: str
    ) -> dict[str, Any]:
        """Stub: simulate envelope encryption with data key wrapping."""
        return {
            "cipher_text": f"ENV_ENC::{plain_text}",
            "wrapped_data_key": f"WRAPPED::{data_key}",
            "key_reference": "master-key-v1",
        }

    async def checksum(self, value: str) -> str:
        """SHA-256 checksum for integrity verification."""
        return hashlib.sha256(value.encode()).hexdigest()

    async def verify_checksum(self, value: str, expected: str) -> bool:
        """Verify integrity by comparing computed to expected checksum."""
        return await self.checksum(value) == expected

    # ── IKeyManager ────────────────────────────────────

    async def get_master_key(self) -> str:
        """Stub: return the active master key reference."""
        return "master-key-v1"

    async def rotate_master_key(self) -> str:
        """Stub: simulate master key rotation."""
        return "master-key-v2"

    async def schedule_rotation(
        self, secret_id: uuid.UUID, interval_days: int
    ) -> bool:
        """Stub: register rotation schedule (persisted via SecretRotation)."""
        rotation = SecretRotation(
            secret_id=secret_id,
            interval_days=interval_days,
        )
        await self.repo.create_rotation(rotation)
        return True
