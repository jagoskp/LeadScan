import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.assets.exceptions import (
    AssetNotFoundException,
    ImmutableAssetModificationException,
)
from services.api.src.assets.integrity import AssetIntegrityValidator
from services.api.src.assets.metadata import AssetMetadataExtractor
from services.api.src.assets.models import Asset, AssetIntegrity, AssetMetadata, AssetVersion, CompanyLogo
from services.api.src.assets.repository import AssetRepository
from services.api.src.assets.service import AssetService
from services.api.src.assets.schemas import AssetCreateSchema
from services.api.src.assets.storage import AssetStorageEngine


def test_storage_engine_and_hashing(tmp_path):
    storage = AssetStorageEngine(base_storage_dir=str(tmp_path))
    payload = b"Sample Image Content Payload"

    sha256 = storage.calculate_sha256(payload)
    md5 = storage.calculate_md5(payload)

    assert len(sha256) == 64
    assert len(md5) == 32

    saved_path = storage.save_raw_file("test.jpg", payload)
    read_payload = storage.read_raw_file(saved_path)
    assert read_payload == payload


def test_metadata_extractor():
    extractor = AssetMetadataExtractor()
    payload = b"Mock File Bytes Data"
    meta = extractor.extract_metadata(payload)

    assert meta["file_size_bytes"] == len(payload)
    assert meta["color_space"] == "RGB"


def test_integrity_validator(tmp_path):
    storage = AssetStorageEngine(base_storage_dir=str(tmp_path))
    validator = AssetIntegrityValidator(storage)

    payload = b"Lossless Storage Integrity Test"
    expected_hash = storage.calculate_sha256(payload)
    saved_path = storage.save_raw_file("scan.png", payload)

    status_str, actual_hash = validator.validate_integrity(saved_path, expected_hash)
    assert status_str == "healthy"
    assert actual_hash == expected_hash


@pytest.fixture
def mock_db():
    db = AsyncMock()
    now = datetime.now(UTC)
    asset_id = uuid.uuid4()
    mock_asset = Asset(
        id=asset_id,
        asset_type="original_scan",
        file_name="card_scan.jpg",
        storage_path="storage/assets/card_scan.jpg",
        mime_type="image/jpeg",
        is_immutable=True,
        created_at=now,
        updated_at=now,
        asset_metadata=AssetMetadata(
            id=uuid.uuid4(),
            asset_id=asset_id,
            file_size_bytes=1024,
            width=800,
            height=600,
            dpi="300 DPI",
            color_space="RGB",
            hash_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            created_at=now,
        ),
        integrity_record=AssetIntegrity(
            id=uuid.uuid4(),
            asset_id=asset_id,
            expected_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            actual_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            integrity_status="healthy",
            last_checked_at=now,
        ),
        versions=[
            AssetVersion(
                id=uuid.uuid4(),
                asset_id=asset_id,
                version_number=1,
                storage_path="storage/assets/card_scan.jpg",
                checksum_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                created_at=now,
            )
        ],
        thumbnails=[],
        audits=[],
    )

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        stmt_str = str(stmt)
        if "company_logos" in stmt_str:
            res.scalars.return_value.first.return_value = None
        else:
            res.scalars.return_value.first.return_value = mock_asset
            res.scalars.return_value.all.return_value = [mock_asset]
        return res

    db.execute.side_effect = mock_execute
    return db


@pytest.mark.asyncio
async def test_upload_and_get_asset(mock_db):
    service = AssetService(mock_db)
    req = AssetCreateSchema(file_name="card_scan.jpg", asset_type="original_scan", is_immutable=True)
    payload = b"Raw Lossless Binary Content"

    result = await service.upload_asset(req, payload)
    assert result.file_name == "card_scan.jpg"
    assert result.is_immutable is True


@pytest.mark.asyncio
async def test_immutable_asset_rollback_prevention(mock_db):
    service = AssetService(mock_db)
    asset_id = uuid.uuid4()

    with pytest.raises(ImmutableAssetModificationException):
        await service.rollback_version(asset_id, 1)


@pytest.mark.asyncio
async def test_company_default_logo_fallback(mock_db):
    service = AssetService(mock_db)
    co_id = uuid.uuid4()

    logo = await service.get_company_logo(co_id)
    assert logo.is_default is True
    assert logo.logo_url == "/assets/default-company-logo.png"
