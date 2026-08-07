import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

from services.api.src.auth.models import User
from services.api.src.storage.exceptions import (
    FileNotFoundException,
    ProviderNotFoundException,
    QuotaExceededException,
    QuotaNotFoundException,
)
from services.api.src.storage.models import StorageFile, StorageProvider, StorageQuota
from services.api.src.storage.repository import (
    StorageFileRepository,
    StorageProviderRepository,
    StorageQuotaRepository,
)
from services.api.src.storage.schemas import (
    StorageFileCreate,
    StorageFileUpdate,
    StorageProviderCreate,
    StorageProviderUpdate,
)


class StorageService:
    """Service orchestrating Storage Provider configurations and Quota tracking."""

    def __init__(
        self,
        provider_repo: StorageProviderRepository,
        file_repo: StorageFileRepository,
        quota_repo: StorageQuotaRepository,
    ) -> None:
        self.provider_repo = provider_repo
        self.file_repo = file_repo
        self.quota_repo = quota_repo

    def _get_user_organization_ids(self, user: User) -> list[uuid.UUID]:
        """Helper to extract organization IDs where the user has active membership."""
        return [m.organization_id for m in getattr(user, "memberships", [])]

    def _is_user_org_admin(self, user: User, org_id: uuid.UUID) -> bool:
        """Helper to check if user has admin/owner role in target organization."""
        memberships = getattr(user, "memberships", [])
        return any(
            m.organization_id == org_id
            and getattr(m, "role", "Member") in ("Owner", "Admin")
            for m in memberships
        )

    # ----------------------------------------------------
    # Storage Providers Lifecycle
    # ----------------------------------------------------

    async def register_provider(
        self, user: User, data: StorageProviderCreate
    ) -> StorageProvider:
        """Register a new storage provider configuration."""
        org_ids = self._get_user_organization_ids(user)
        if data.organization_id and data.organization_id not in org_ids:
            raise ProviderNotFoundException()

        provider = StorageProvider(
            organization_id=data.organization_id,
            name=data.name,
            provider_type=data.provider_type.value,
            bucket_name=data.bucket_name,
            region=data.region,
            endpoint_url=data.endpoint_url,
            is_active=data.is_active,
            is_default=data.is_default,
        )
        return await self.provider_repo.create(provider)

    async def get_provider(self, provider_id: uuid.UUID, user: User) -> StorageProvider:
        """Retrieve storage provider details, enforcing membership boundaries."""
        provider = await self.provider_repo.get_by_id(provider_id)
        if not provider:
            raise ProviderNotFoundException()

        org_ids = self._get_user_organization_ids(user)
        if provider.organization_id and provider.organization_id not in org_ids:
            raise ProviderNotFoundException()

        return provider

    async def list_providers(
        self, user: User, organization_id: uuid.UUID | None = None
    ) -> Sequence[StorageProvider]:
        """List active storage providers configured for the user scope."""
        org_ids = self._get_user_organization_ids(user)
        if organization_id and organization_id not in org_ids:
            organization_id = None

        return await self.provider_repo.list_providers(organization_id)

    async def update_provider(
        self, provider_id: uuid.UUID, user: User, data: StorageProviderUpdate
    ) -> StorageProvider:
        """Update configurations of an existing storage provider."""
        await self.get_provider(provider_id, user)

        update_dict = data.model_dump(exclude_unset=True)
        if "provider_type" in update_dict and update_dict["provider_type"] is not None:
            update_dict["provider_type"] = update_dict["provider_type"].value
        if "health_status" in update_dict and update_dict["health_status"] is not None:
            update_dict["health_status"] = update_dict["health_status"].value

        updated = await self.provider_repo.update(provider_id, update_dict)
        if not updated:
            raise ProviderNotFoundException()
        return updated

    async def delete_provider(self, provider_id: uuid.UUID, user: User) -> None:
        """Delete storage provider configuration."""
        await self.get_provider(provider_id, user)
        await self.provider_repo.delete(provider_id)

    async def check_health(self, provider_id: uuid.UUID, user: User) -> StorageProvider:
        """Simulate and register storage health checks."""
        await self.get_provider(provider_id, user)
        health_data = {
            "health_status": "HEALTHY",
            "health_checked_at": datetime.now(UTC),
        }
        updated = await self.provider_repo.update(provider_id, health_data)
        if not updated:
            raise ProviderNotFoundException()
        return updated

    # ----------------------------------------------------
    # Storage Quotas & Usage Tracking
    # ----------------------------------------------------

    async def get_quota(self, user: User, organization_id: uuid.UUID) -> StorageQuota:
        """Retrieve quota profile context for an organization."""
        org_ids = self._get_user_organization_ids(user)
        if organization_id not in org_ids:
            raise QuotaNotFoundException()

        quota = await self.quota_repo.get_by_org_id(organization_id)
        if not quota:
            quota = await self.quota_repo.create_default(organization_id)
        return quota

    async def update_quota_limit(
        self, user: User, organization_id: uuid.UUID, max_bytes: int
    ) -> StorageQuota:
        """Modify maximum bytes allocation limit for an organization (admin only)."""
        org_ids = self._get_user_organization_ids(user)
        if organization_id not in org_ids:
            raise QuotaNotFoundException()

        if not self._is_user_org_admin(user, organization_id):
            raise QuotaNotFoundException()

        return await self.quota_repo.update_quota(organization_id, max_bytes)

    async def verify_quota_availability(
        self, organization_id: uuid.UUID, file_size: int
    ) -> StorageQuota:
        """Ensure file registration does not exceed storage limits."""
        quota = await self.quota_repo.get_by_org_id(organization_id)
        if not quota:
            quota = await self.quota_repo.create_default(organization_id)

        if quota.used_bytes + file_size > quota.max_bytes:
            raise QuotaExceededException(
                "Storage limit exceeded. Available: "
                f"{quota.max_bytes - quota.used_bytes} bytes."
            )
        return quota

    # ----------------------------------------------------
    # Storage File Operations (Metadata only)
    # ----------------------------------------------------

    async def register_file(self, user: User, data: StorageFileCreate) -> StorageFile:
        """Register file metadata, deducting allocated quota bytes."""
        org_ids = self._get_user_organization_ids(user)
        if data.organization_id not in org_ids:
            raise FileNotFoundException()

        # Check quota availability
        await self.verify_quota_availability(data.organization_id, data.file_size)

        file_rec = StorageFile(
            document_id=data.document_id,
            user_id=data.user_id,
            organization_id=data.organization_id,
            storage_provider_id=data.storage_provider_id,
            storage_path=data.storage_path,
            file_size=data.file_size,
            mime_type=data.mime_type,
            original_filename=data.original_filename,
            status="ACTIVE",
            metadata_log=data.metadata_log,
        )

        created_file = await self.file_repo.create(file_rec)

        # Increment usage statistics
        await self.quota_repo.adjust_usage(
            organization_id=data.organization_id,
            bytes_delta=data.file_size,
            files_delta=1,
        )

        return created_file

    async def get_file(self, file_id: uuid.UUID, user: User) -> StorageFile:
        """Retrieve a specific file metadata record."""
        file_rec = await self.file_repo.get_by_id(file_id)
        if not file_rec:
            raise FileNotFoundException()

        org_ids = self._get_user_organization_ids(user)
        if file_rec.organization_id not in org_ids:
            raise FileNotFoundException()

        return file_rec

    async def list_files(
        self,
        user: User,
        organization_id: uuid.UUID,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[StorageFile], int]:
        """List files registered within an organization context."""
        org_ids = self._get_user_organization_ids(user)
        if organization_id not in org_ids:
            raise FileNotFoundException()

        return await self.file_repo.list_files(
            organization_id=organization_id, status=status, skip=skip, limit=limit
        )

    async def update_file_metadata(
        self, file_id: uuid.UUID, user: User, data: StorageFileUpdate
    ) -> StorageFile:
        """Update metadata on an existing file registry."""
        await self.get_file(file_id, user)

        update_dict = data.model_dump(exclude_unset=True)
        if "status" in update_dict and update_dict["status"] is not None:
            update_dict["status"] = update_dict["status"].value

        updated = await self.file_repo.update(file_id, update_dict)
        if not updated:
            raise FileNotFoundException()
        return updated

    async def soft_delete_file(self, file_id: uuid.UUID, user: User) -> StorageFile:
        """Mark a file as soft-deleted, releasing quota consumption allocation."""
        file_rec = await self.get_file(file_id, user)
        if file_rec.status == "SOFT_DELETED":
            return file_rec

        # Shift status and register date
        del_data = {
            "status": "SOFT_DELETED",
            "deleted_at": datetime.now(UTC),
        }
        updated = await self.file_repo.update(file_id, del_data)
        if not updated:
            raise FileNotFoundException()

        # Release quota space (negative adjustment)
        await self.quota_repo.adjust_usage(
            organization_id=file_rec.organization_id,
            bytes_delta=-file_rec.file_size,
            files_delta=-1,
        )
        return updated

    async def restore_file(self, file_id: uuid.UUID, user: User) -> StorageFile:
        """Restore a soft-deleted file, re-verifying and claiming quota usage."""
        file_rec = await self.get_file(file_id, user)
        if file_rec.status != "SOFT_DELETED":
            return file_rec

        # Ensure quota available to hold restored file
        await self.verify_quota_availability(
            file_rec.organization_id, file_rec.file_size
        )

        restore_data = {
            "status": "ACTIVE",
            "deleted_at": None,
        }
        updated = await self.file_repo.update(file_id, restore_data)
        if not updated:
            raise FileNotFoundException()

        # Re-increment quota space
        await self.quota_repo.adjust_usage(
            organization_id=file_rec.organization_id,
            bytes_delta=file_rec.file_size,
            files_delta=1,
        )
        return updated

    async def cleanup_file(self, file_id: uuid.UUID, user: User) -> StorageFile:
        """Clean metadata logs, declaring final cleanup state."""
        await self.get_file(file_id, user)
        cleanup_data = {
            "status": "CLEANED",
        }
        updated = await self.file_repo.update(file_id, cleanup_data)
        if not updated:
            raise FileNotFoundException()
        return updated

    async def delete_file_metadata(self, file_id: uuid.UUID, user: User) -> None:
        """Hard delete metadata logs from DB."""
        file_rec = await self.get_file(file_id, user)

        # If file was active, reclaim quota space before deleting metadata log
        if file_rec.status == "ACTIVE":
            await self.quota_repo.adjust_usage(
                organization_id=file_rec.organization_id,
                bytes_delta=-file_rec.file_size,
                files_delta=-1,
            )

        await self.file_repo.delete(file_id)
