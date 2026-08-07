from abc import ABC, abstractmethod
from typing import Any
import uuid

from services.api.src.assets.schemas import (
    AssetCreateSchema,
    AssetIntegritySchema,
    AssetSchema,
    AssetVersionSchema,
    CompanyLogoSchema,
)


class IAssetRepository(ABC):
    """Abstract interface for Asset persistence operations."""

    @abstractmethod
    async def get_by_id(self, asset_id: uuid.UUID) -> Any:
        pass

    @abstractmethod
    async def save(self, asset: Any) -> Any:
        pass


class IAssetService(ABC):
    """Abstract interface for DAM engine service operations."""

    @abstractmethod
    async def upload_asset(
        self,
        request: AssetCreateSchema,
        file_bytes: bytes,
        owner_id: uuid.UUID | None = None,
    ) -> AssetSchema:
        pass

    @abstractmethod
    async def get_asset(self, asset_id: uuid.UUID) -> AssetSchema:
        pass

    @abstractmethod
    async def verify_integrity(self, asset_id: uuid.UUID) -> AssetIntegritySchema:
        pass

    @abstractmethod
    async def rollback_version(self, asset_id: uuid.UUID, version_number: int) -> AssetSchema:
        pass

    @abstractmethod
    async def get_company_logo(self, company_id: uuid.UUID) -> CompanyLogoSchema:
        pass
