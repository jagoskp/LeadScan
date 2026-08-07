import base64
import logging
from typing import Any
import uuid
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.assets.exceptions import AssetException
from services.api.src.assets.schemas import (
    AssetCreateSchema,
    AssetIntegritySchema,
    AssetSchema,
    CompanyLogoSchema,
)
from services.api.src.assets.service import AssetService
from services.api.src.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/assets", tags=["Enterprise Digital Asset Management"])


class AssetUploadPayload(BaseModel):
    file_name: str
    file_data_base64: str
    mime_type: str = "image/jpeg"
    asset_type: str = "original_scan"
    is_immutable: bool = False
    lead_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None


@router.post("/upload", response_model=AssetSchema, status_code=status.HTTP_201_CREATED)
async def upload_asset(
    payload: AssetUploadPayload,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """Upload raw binary asset losslessly with hash computation and derivative thumbnail generation."""
    try:
        file_bytes = base64.b64decode(payload.file_data_base64)
        req = AssetCreateSchema(
            asset_type=payload.asset_type,
            file_name=payload.file_name,
            mime_type=payload.mime_type,
            is_immutable=payload.is_immutable,
            lead_id=payload.lead_id,
            company_id=payload.company_id,
        )
        service = AssetService(db)
        return await service.upload_asset(req, file_bytes, owner_id=user_id)
    except Exception as exc:
        if isinstance(exc, AssetException):
            raise HTTPException(status_code=exc.status_code, detail=exc.message)
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=list[AssetSchema])
async def list_assets(
    asset_type: str | None = Query(default=None),
    lead_id: uuid.UUID | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List digital assets from the DAM repository."""
    service = AssetService(db)
    return await service.list_assets(asset_type=asset_type, lead_id=lead_id, limit=limit)


@router.get("/{asset_id}", response_model=AssetSchema)
async def get_asset(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get single asset metadata, versions, and integrity status."""
    try:
        service = AssetService(db)
        return await service.get_asset(asset_id)
    except AssetException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/{asset_id}/verify-integrity", response_model=AssetIntegritySchema)
async def verify_asset_integrity(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Verify SHA256 checksum integrity of an asset file on disk."""
    try:
        service = AssetService(db)
        return await service.verify_integrity(asset_id)
    except AssetException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/{asset_id}/rollback", response_model=AssetSchema)
async def rollback_asset_version(
    asset_id: uuid.UUID,
    version_number: int = Query(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Rollback non-immutable asset to a previous version."""
    try:
        service = AssetService(db)
        return await service.rollback_version(asset_id, version_number)
    except AssetException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/company-logo/{company_id}", response_model=CompanyLogoSchema)
async def get_company_logo(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get company custom logo or automatic system default fallback logo."""
    service = AssetService(db)
    return await service.get_company_logo(company_id)
