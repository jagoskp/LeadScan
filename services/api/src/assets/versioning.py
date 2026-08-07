from datetime import UTC, datetime
from typing import Any
import uuid

from services.api.src.assets.exceptions import ImmutableAssetModificationException
from services.api.src.assets.models import Asset, AssetVersion


class AssetVersioningEngine:
    """Versioning Engine managing version history and rollback operations."""

    def create_version(
        self, asset: Asset, storage_path: str, checksum_sha256: str
    ) -> AssetVersion:
        if asset.is_immutable:
            raise ImmutableAssetModificationException(str(asset.id))

        new_version_num = len(asset.versions) + 1 if asset.versions else 1
        v_obj = AssetVersion(
            id=uuid.uuid4(),
            asset_id=asset.id,
            version_number=new_version_num,
            storage_path=storage_path,
            checksum_sha256=checksum_sha256,
            created_at=datetime.now(UTC),
        )
        return v_obj
