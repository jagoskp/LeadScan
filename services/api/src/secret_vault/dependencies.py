# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.secret_vault.repository import SecretRepository
from services.api.src.secret_vault.service import SecretVaultService


def get_secret_repository(
    session: AsyncSession = Depends(get_db),
) -> SecretRepository:
    """Inject SecretRepository context."""
    return SecretRepository(session)


def get_secret_vault_service(
    repo: SecretRepository = Depends(get_secret_repository),
) -> SecretVaultService:
    """Inject SecretVaultService context."""
    return SecretVaultService(repo)
