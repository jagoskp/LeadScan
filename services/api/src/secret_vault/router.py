# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.secret_vault.dependencies import get_secret_vault_service
from services.api.src.secret_vault.schemas import (
    SecretAccessCreate,
    SecretAccessResponse,
    SecretAuditResponse,
    SecretCreate,
    SecretPolicyCreate,
    SecretPolicyResponse,
    SecretResponse,
    SecretRotateRequest,
    SecretVersionResponse,
)
from services.api.src.secret_vault.service import SecretVaultService

router = APIRouter(prefix="/vault", tags=["secret_vault"])


# ── Secrets CRUD ───────────────────────────────────────

@router.post(
    "/secrets",
    response_model=SecretResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_secret(
    payload: SecretCreate,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Encrypt and store a new secret in the vault."""
    return await service.create_from_schema(payload, current_user.id)


@router.get("/secrets", response_model=list[SecretResponse])
async def list_secrets(
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """List secret identities (never decrypted values)."""
    return await service.list_secrets()


@router.get("/secrets/{secret_id}", response_model=SecretResponse)
async def get_secret(
    secret_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Retrieve secret metadata (never the raw value)."""
    return await service.get_secret(secret_id)


@router.delete(
    "/secrets/{secret_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_secret(
    secret_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> None:
    """Permanently delete a secret and all its versions."""
    await service.delete_secret(secret_id, current_user.id)


# ── Lifecycle ──────────────────────────────────────────

@router.post("/secrets/{secret_id}/rotate")
async def rotate_secret(
    secret_id: uuid.UUID,
    payload: SecretRotateRequest,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Re-encrypt the secret with a new value, creating a new version."""
    new_version = await service.rotate_secret(
        secret_id, payload.new_plain_value, current_user.id
    )
    return {"secret_id": secret_id, "new_version": new_version}


@router.post("/secrets/{secret_id}/archive")
async def archive_secret(
    secret_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Archive a secret, making it inaccessible without recovery."""
    success = await service.archive_secret(secret_id, current_user.id)
    return {"success": success}


@router.post("/secrets/{secret_id}/recover")
async def recover_secret(
    secret_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Recover an archived secret back to active status."""
    success = await service.recover_secret(secret_id, current_user.id)
    return {"success": success}


# ── Versions ───────────────────────────────────────────

@router.get(
    "/secrets/{secret_id}/versions",
    response_model=list[SecretVersionResponse],
)
async def list_secret_versions(
    secret_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """List version history for a secret (no decrypted values)."""
    secret = await service.get_secret(secret_id)
    return secret.versions


# ── Access Grants ──────────────────────────────────────

@router.post(
    "/secrets/{secret_id}/access",
    response_model=SecretAccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def grant_access(
    secret_id: uuid.UUID,
    payload: SecretAccessCreate,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Grant scoped access to a secret for a user or connector."""
    return await service.grant_access(secret_id, payload, current_user.id)


# ── Policy ─────────────────────────────────────────────

@router.post(
    "/secrets/{secret_id}/policy",
    response_model=SecretPolicyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def set_secret_policy(
    secret_id: uuid.UUID,
    payload: SecretPolicyCreate,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Set rotation and retention policy for a secret."""
    return await service.set_policy(secret_id, payload)


# ── Audit ──────────────────────────────────────────────

@router.get(
    "/secrets/{secret_id}/audit",
    response_model=list[SecretAuditResponse],
)
async def get_secret_audit(
    secret_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Retrieve full audit trail for a secret."""
    secret = await service.get_secret(secret_id)
    return secret.audit_logs


# ── Key Management ─────────────────────────────────────

@router.post("/keys/rotate")
async def rotate_master_key(
    current_user: User = Depends(get_current_user),
    service: SecretVaultService = Depends(get_secret_vault_service),
) -> Any:
    """Trigger a master encryption key rotation."""
    new_key_ref = await service.rotate_master_key()
    return {"new_key_reference": new_key_ref}
