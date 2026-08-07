import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.assets.models import (
    Asset,
    AssetAudit,
    AssetIntegrity,
    AssetMetadata,
    AssetThumbnail,
    AssetVersion,
    CompanyLogo,
)

logger = logging.getLogger(__name__)


class AssetRepository:
    """Repository handling persistence operations for Digital Asset Management data models."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, asset_id: uuid.UUID) -> Asset | None:
        stmt = (
            select(Asset)
            .options(
                selectinload(Asset.asset_metadata),
                selectinload(Asset.integrity_record),
                selectinload(Asset.versions),
                selectinload(Asset.thumbnails),
                selectinload(Asset.audits),
            )
            .where(Asset.id == asset_id)
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def list_assets(
        self, asset_type: str | None = None, lead_id: uuid.UUID | None = None, limit: int = 50
    ) -> Sequence[Asset]:
        stmt = select(Asset).options(
            selectinload(Asset.asset_metadata),
            selectinload(Asset.integrity_record),
            selectinload(Asset.thumbnails),
        )

        if asset_type:
            stmt = stmt.where(Asset.asset_type == asset_type)
        if lead_id:
            stmt = stmt.where(Asset.lead_id == lead_id)

        stmt = stmt.order_by(Asset.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def get_company_logo(self, company_id: uuid.UUID) -> CompanyLogo | None:
        stmt = select(CompanyLogo).where(CompanyLogo.company_id == company_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()
