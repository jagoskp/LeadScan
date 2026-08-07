import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import and_, delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.storage.models import StorageFile, StorageProvider, StorageQuota


class StorageProviderRepository:
    """Repository handling database persistence operations for StorageProviders."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def clear_defaults(self, organization_id: uuid.UUID | None) -> None:
        """Reset is_default to False for all providers in the given scope."""
        stmt = update(StorageProvider).values(is_default=False)
        if organization_id:
            stmt = stmt.where(StorageProvider.organization_id == organization_id)
        else:
            stmt = stmt.where(StorageProvider.organization_id.is_(None))
        await self.session.execute(stmt)

    async def create(self, provider: StorageProvider) -> StorageProvider:
        """Persist a new StorageProvider record, ensuring single default logic."""
        if provider.is_default:
            await self.clear_defaults(provider.organization_id)
        self.session.add(provider)
        await self.session.flush()
        return provider

    async def get_by_id(self, provider_id: uuid.UUID) -> StorageProvider | None:
        """Retrieve a StorageProvider record by ID."""
        result = await self.session.execute(
            select(StorageProvider).where(StorageProvider.id == provider_id)
        )
        return result.scalar_one_or_none()

    async def get_default(
        self, organization_id: uuid.UUID | None
    ) -> StorageProvider | None:
        """Fetch the default configured provider for an organization or system."""
        stmt = select(StorageProvider).where(StorageProvider.is_default.is_(True))
        if organization_id:
            stmt = stmt.where(
                or_(
                    StorageProvider.organization_id == organization_id,
                    StorageProvider.organization_id.is_(None),
                )
            ).order_by(
                # Org overrides system-wide default
                StorageProvider.organization_id.desc()
            )
        else:
            stmt = stmt.where(StorageProvider.organization_id.is_(None))

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_providers(
        self, organization_id: uuid.UUID | None = None
    ) -> Sequence[StorageProvider]:
        """List active storage providers available in a given scope."""
        stmt = select(StorageProvider).where(StorageProvider.is_active.is_(True))
        if organization_id:
            stmt = stmt.where(
                or_(
                    StorageProvider.organization_id == organization_id,
                    StorageProvider.organization_id.is_(None),
                )
            )
        else:
            stmt = stmt.where(StorageProvider.organization_id.is_(None))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(
        self, provider_id: uuid.UUID, data: dict[str, Any]
    ) -> StorageProvider | None:
        """Update fields on an existing provider."""
        if data:
            if data.get("is_default"):
                provider = await self.get_by_id(provider_id)
                if provider:
                    await self.clear_defaults(provider.organization_id)

            data["updated_at"] = datetime.now(UTC)
            await self.session.execute(
                update(StorageProvider)
                .where(StorageProvider.id == provider_id)
                .values(**data)
            )
        return await self.get_by_id(provider_id)

    async def delete(self, provider_id: uuid.UUID) -> bool:
        """Delete a StorageProvider record."""
        result = await self.session.execute(
            delete(StorageProvider).where(StorageProvider.id == provider_id)
        )
        rowcount = getattr(result, "rowcount", 0)
        return rowcount > 0


class StorageFileRepository:
    """Repository handling database operations for StorageFiles."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, file: StorageFile) -> StorageFile:
        """Persist a new StorageFile metadata record."""
        self.session.add(file)
        await self.session.flush()
        return file

    async def get_by_id(self, file_id: uuid.UUID) -> StorageFile | None:
        """Retrieve a StorageFile record by ID."""
        result = await self.session.execute(
            select(StorageFile).where(StorageFile.id == file_id)
        )
        return result.scalar_one_or_none()

    async def list_files(
        self,
        organization_id: uuid.UUID,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[StorageFile], int]:
        """List files registered within an organization context."""
        conditions = [StorageFile.organization_id == organization_id]
        if status:
            conditions.append(StorageFile.status == status)

        base_filter = and_(*conditions)

        # Count total
        count_stmt = select(func.count()).select_from(StorageFile).where(base_filter)
        count_res = await self.session.execute(count_stmt)
        total = count_res.scalar() or 0

        # Retrieve records
        stmt = (
            select(StorageFile)
            .where(base_filter)
            .order_by(StorageFile.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def update(
        self, file_id: uuid.UUID, data: dict[str, Any]
    ) -> StorageFile | None:
        """Update fields on an existing file."""
        if data:
            data["updated_at"] = datetime.now(UTC)
            await self.session.execute(
                update(StorageFile).where(StorageFile.id == file_id).values(**data)
            )
        return await self.get_by_id(file_id)

    async def delete(self, file_id: uuid.UUID) -> bool:
        """Hard delete a StorageFile metadata record."""
        result = await self.session.execute(
            delete(StorageFile).where(StorageFile.id == file_id)
        )
        rowcount = getattr(result, "rowcount", 0)
        return rowcount > 0


class StorageQuotaRepository:
    """Repository handling database operations for StorageQuotas."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_org_id(self, organization_id: uuid.UUID) -> StorageQuota | None:
        """Fetch the storage quota limit profile for an organization."""
        result = await self.session.execute(
            select(StorageQuota).where(StorageQuota.organization_id == organization_id)
        )
        return result.scalar_one_or_none()

    async def create_default(self, organization_id: uuid.UUID) -> StorageQuota:
        """Persist a default storage quota configuration profile."""
        quota = StorageQuota(
            organization_id=organization_id,
            max_bytes=53687091200,  # 50 GB default limit
            used_bytes=0,
            file_count=0,
        )
        self.session.add(quota)
        await self.session.flush()
        return quota

    async def update_quota(
        self, organization_id: uuid.UUID, max_bytes: int
    ) -> StorageQuota:
        """Update max bytes limit for an organization, creating profile if missing."""
        quota = await self.get_by_org_id(organization_id)
        if not quota:
            quota = StorageQuota(
                organization_id=organization_id,
                max_bytes=max_bytes,
                used_bytes=0,
                file_count=0,
            )
            self.session.add(quota)
        else:
            quota.max_bytes = max_bytes
            quota.updated_at = datetime.now(UTC)

        await self.session.flush()
        return quota

    async def adjust_usage(
        self, organization_id: uuid.UUID, bytes_delta: int, files_delta: int
    ) -> StorageQuota | None:
        """Adjust accumulated usage statistics, capping values at zero."""
        quota = await self.get_by_org_id(organization_id)
        if not quota:
            quota = await self.create_default(organization_id)

        quota.used_bytes += bytes_delta
        quota.file_count += files_delta

        if quota.used_bytes < 0:
            quota.used_bytes = 0
        if quota.file_count < 0:
            quota.file_count = 0

        quota.updated_at = datetime.now(UTC)
        await self.session.flush()
        return quota
