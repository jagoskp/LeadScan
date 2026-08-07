import logging
from datetime import UTC, datetime
from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.assets.exceptions import (
    AssetNotFoundException,
    ImmutableAssetModificationException,
)
from services.api.src.assets.integrity import AssetIntegrityValidator
from services.api.src.assets.interfaces import IAssetService
from services.api.src.assets.metadata import AssetMetadataExtractor
from services.api.src.assets.models import (
    Asset,
    AssetAudit,
    AssetIntegrity,
    AssetMetadata,
    AssetThumbnail,
    AssetVersion,
    CompanyLogo,
)
from services.api.src.assets.repository import AssetRepository
from services.api.src.assets.schemas import (
    AssetCreateSchema,
    AssetIntegritySchema,
    AssetMetadataSchema,
    AssetSchema,
    AssetThumbnailSchema,
    AssetVersionSchema,
    CompanyLogoSchema,
)
from services.api.src.assets.storage import AssetStorageEngine
from services.api.src.assets.thumbnail import ThumbnailGenerator
from services.api.src.assets.validators import validate_asset_upload
from services.api.src.assets.versioning import AssetVersioningEngine

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_LOGO_URL = "/assets/default-company-logo.png"


class AssetService(IAssetService):
    """Facade Service for Enterprise Digital Asset Management Engine."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AssetRepository(db)
        self.storage = AssetStorageEngine()
        self.metadata_extractor = AssetMetadataExtractor()
        self.integrity_validator = AssetIntegrityValidator(self.storage)
        self.versioning_engine = AssetVersioningEngine()
        self.thumbnail_generator = ThumbnailGenerator(self.storage)

    async def upload_asset(
        self,
        request: AssetCreateSchema,
        file_bytes: bytes,
        owner_id: uuid.UUID | None = None,
    ) -> AssetSchema:
        file_name, mime_type = validate_asset_upload(request.file_name, request.mime_type, file_bytes)

        # 1. Lossless Raw File Storage & Hashes
        sha256_hash = self.storage.calculate_sha256(file_bytes)
        md5_hash = self.storage.calculate_md5(file_bytes)
        raw_storage_path = self.storage.save_raw_file(file_name, file_bytes)

        # 2. Extract Metadata
        meta_dict = self.metadata_extractor.extract_metadata(file_bytes)

        now = datetime.now(UTC)
        is_original_scan = request.asset_type == "original_scan" or request.is_immutable

        # 3. Create Core Asset Model
        asset = Asset(
            id=uuid.uuid4(),
            lead_id=request.lead_id,
            company_id=request.company_id,
            contact_id=request.contact_id,
            review_session_id=request.review_session_id,
            ocr_result_id=request.ocr_result_id,
            owner_id=owner_id,
            asset_type=request.asset_type,
            file_name=file_name,
            storage_path=raw_storage_path,
            mime_type=mime_type,
            is_immutable=is_original_scan,
            created_at=now,
            updated_at=now,
        )
        self.db.add(asset)
        await self.db.flush()

        # 4. Create AssetMetadata
        meta_obj = AssetMetadata(
            id=uuid.uuid4(),
            asset_id=asset.id,
            file_size_bytes=meta_dict["file_size_bytes"],
            width=meta_dict["width"],
            height=meta_dict["height"],
            dpi=meta_dict["dpi"],
            color_space=meta_dict["color_space"],
            hash_sha256=sha256_hash,
            checksum_md5=md5_hash,
            created_at=now,
        )
        self.db.add(meta_obj)

        # 5. Create AssetIntegrity Record
        integrity_obj = AssetIntegrity(
            id=uuid.uuid4(),
            asset_id=asset.id,
            expected_hash=sha256_hash,
            actual_hash=sha256_hash,
            integrity_status="healthy",
            last_checked_at=now,
        )
        self.db.add(integrity_obj)

        # 6. Create Initial Version
        initial_version = AssetVersion(
            id=uuid.uuid4(),
            asset_id=asset.id,
            version_number=1,
            storage_path=raw_storage_path,
            checksum_sha256=sha256_hash,
            created_at=now,
        )
        self.db.add(initial_version)

        # 7. Generate Thumbnails / Previews without altering original
        thumbnails = self.thumbnail_generator.generate_thumbnails(file_bytes, file_name)
        for t in thumbnails:
            t_obj = AssetThumbnail(
                id=uuid.uuid4(),
                asset_id=asset.id,
                thumbnail_type=t["thumbnail_type"],
                width=t["width"],
                height=t["height"],
                storage_path=t["storage_path"],
                created_at=now,
            )
            self.db.add(t_obj)

        # 8. Audit Record
        audit_obj = AssetAudit(
            id=uuid.uuid4(),
            asset_id=asset.id,
            action_type="upload",
            actor_id=owner_id,
            details={"file_name": file_name, "file_size": len(file_bytes)},
            created_at=now,
        )
        self.db.add(audit_obj)

        await self.db.commit()
        full_asset = await self.repo.get_by_id(asset.id)
        if not full_asset:
            raise AssetNotFoundException(str(asset.id))
        return self._to_schema(full_asset)

    async def get_asset(self, asset_id: uuid.UUID) -> AssetSchema:
        asset = await self.repo.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundException(str(asset_id))
        return self._to_schema(asset)

    async def list_assets(
        self, asset_type: str | None = None, lead_id: uuid.UUID | None = None, limit: int = 50
    ) -> list[AssetSchema]:
        assets = await self.repo.list_assets(asset_type, lead_id, limit)
        return [self._to_schema(a) for a in assets]

    async def verify_integrity(self, asset_id: uuid.UUID) -> AssetIntegritySchema:
        asset = await self.repo.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundException(str(asset_id))

        status_str, actual_hash = self.integrity_validator.validate_integrity(
            asset.storage_path, asset.integrity_record.expected_hash if asset.integrity_record else ""
        )

        if asset.integrity_record:
            asset.integrity_record.integrity_status = status_str
            asset.integrity_record.actual_hash = actual_hash
            asset.integrity_record.last_checked_at = datetime.now(UTC)

        await self.db.commit()
        return AssetIntegritySchema.model_validate(asset.integrity_record)

    async def rollback_version(self, asset_id: uuid.UUID, version_number: int) -> AssetSchema:
        asset = await self.repo.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundException(str(asset_id))
        if asset.is_immutable:
            raise ImmutableAssetModificationException(str(asset_id))

        target_v = next((v for v in asset.versions if v.version_number == version_number), None)
        if not target_v:
            raise AssetNotFoundException(f"Version {version_number} for asset {asset_id}")

        asset.storage_path = target_v.storage_path
        asset.updated_at = datetime.now(UTC)

        audit_obj = AssetAudit(
            id=uuid.uuid4(),
            asset_id=asset.id,
            action_type="version_rollback",
            details={"rollback_to_version": version_number},
            created_at=datetime.now(UTC),
        )
        self.db.add(audit_obj)

        await self.db.commit()
        full_asset = await self.repo.get_by_id(asset.id)
        if not full_asset:
            raise AssetNotFoundException(str(asset.id))
        return self._to_schema(full_asset)

    async def get_company_logo(self, company_id: uuid.UUID) -> CompanyLogoSchema:
        """Get company custom logo or return default system logo fallback."""
        logo_obj = await self.repo.get_company_logo(company_id)
        if not logo_obj:
            now = datetime.now(UTC)
            logo_obj = CompanyLogo(
                id=uuid.uuid4(),
                company_id=company_id,
                asset_id=None,
                is_default=True,
                logo_url=DEFAULT_SYSTEM_LOGO_URL,
                created_at=now,
            )
            self.db.add(logo_obj)
            await self.db.commit()
        return CompanyLogoSchema.model_validate(logo_obj)

    def _to_schema(self, asset: Asset) -> AssetSchema:
        meta_s = AssetMetadataSchema.model_validate(asset.asset_metadata) if asset.asset_metadata else None
        integ_s = AssetIntegritySchema.model_validate(asset.integrity_record) if asset.integrity_record else None
        vers_s = [AssetVersionSchema.model_validate(v) for v in asset.versions]
        thumbs_s = [AssetThumbnailSchema.model_validate(t) for t in asset.thumbnails]

        return AssetSchema(
            id=asset.id,
            lead_id=asset.lead_id,
            company_id=asset.company_id,
            contact_id=asset.contact_id,
            review_session_id=asset.review_session_id,
            ocr_result_id=asset.ocr_result_id,
            owner_id=asset.owner_id,
            asset_type=asset.asset_type,
            file_name=asset.file_name,
            storage_path=asset.storage_path,
            mime_type=asset.mime_type,
            is_immutable=asset.is_immutable,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            asset_metadata=meta_s,
            integrity_record=integ_s,
            versions=vers_s,
            thumbnails=thumbs_s,
        )
