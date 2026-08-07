import uuid
from collections.abc import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.secret_vault.models import (
    Secret,
    SecretAccess,
    SecretAudit,
    SecretMetadata,
    SecretPolicy,
    SecretRotation,
    SecretVersion,
)


class SecretRepository:
    """Repository handling all vault persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ── Secret CRUD ────────────────────────────────────

    async def create_secret(self, secret: Secret) -> Secret:
        self.session.add(secret)
        await self.session.flush()
        return secret

    async def get_by_id(self, secret_id: uuid.UUID) -> Secret | None:
        stmt = (
            select(Secret)
            .where(Secret.id == secret_id)
            .options(
                selectinload(Secret.versions),
                selectinload(Secret.audit_logs),
                selectinload(Secret.rotations),
                selectinload(Secret.access_grants),
                selectinload(Secret.policy),
                selectinload(Secret.metadata_tags),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_secrets(self) -> Sequence[Secret]:
        stmt = select(Secret)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(
        self, secret_id: uuid.UUID, new_status: str
    ) -> Secret | None:
        stmt = (
            update(Secret)
            .where(Secret.id == secret_id)
            .values(status=new_status)
        )
        await self.session.execute(stmt)
        return await self.get_by_id(secret_id)

    async def delete_secret(self, secret_id: uuid.UUID) -> bool:
        stmt = delete(Secret).where(Secret.id == secret_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))

    # ── SecretVersion ──────────────────────────────────

    async def create_version(
        self, version: SecretVersion
    ) -> SecretVersion:
        self.session.add(version)
        await self.session.flush()
        return version

    async def deactivate_versions(self, secret_id: uuid.UUID) -> None:
        stmt = (
            update(SecretVersion)
            .where(SecretVersion.secret_id == secret_id)
            .values(is_active=False)
        )
        await self.session.execute(stmt)

    async def get_active_version(
        self, secret_id: uuid.UUID
    ) -> SecretVersion | None:
        stmt = (
            select(SecretVersion)
            .where(
                SecretVersion.secret_id == secret_id,
                SecretVersion.is_active.is_(True),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def count_versions(self, secret_id: uuid.UUID) -> int:
        stmt = select(SecretVersion).where(
            SecretVersion.secret_id == secret_id
        )
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    # ── Audit ──────────────────────────────────────────

    async def create_audit(self, audit: SecretAudit) -> SecretAudit:
        self.session.add(audit)
        await self.session.flush()
        return audit

    # ── Rotation ───────────────────────────────────────

    async def create_rotation(
        self, rotation: SecretRotation
    ) -> SecretRotation:
        self.session.add(rotation)
        await self.session.flush()
        return rotation

    # ── Access ─────────────────────────────────────────

    async def create_access(
        self, access: SecretAccess
    ) -> SecretAccess:
        self.session.add(access)
        await self.session.flush()
        return access

    async def get_access_for_requester(
        self,
        secret_id: uuid.UUID,
        requester_id: uuid.UUID,
    ) -> SecretAccess | None:
        stmt = select(SecretAccess).where(
            SecretAccess.secret_id == secret_id,
            SecretAccess.grantee_user_id == requester_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # ── Policy ─────────────────────────────────────────

    async def create_policy(
        self, policy: SecretPolicy
    ) -> SecretPolicy:
        self.session.add(policy)
        await self.session.flush()
        return policy

    # ── Metadata ───────────────────────────────────────

    async def create_metadata(
        self, metadata: SecretMetadata
    ) -> SecretMetadata:
        self.session.add(metadata)
        await self.session.flush()
        return metadata
