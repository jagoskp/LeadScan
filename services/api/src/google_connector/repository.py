import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.google_connector.models import (
    GoogleAccount,
    GoogleSyncHistory,
    GoogleSyncJob,
    MappingValidation,
    RemappingSuggestion,
    Spreadsheet,
    Worksheet,
)

logger = logging.getLogger(__name__)


class GoogleConnectorRepository:
    """Repository handling persistence operations for Google Sheets Connector data models."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_account_by_id(self, account_id: uuid.UUID) -> GoogleAccount | None:
        stmt = select(GoogleAccount).where(GoogleAccount.id == account_id, GoogleAccount.is_active == True)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def list_user_accounts(self, user_id: uuid.UUID) -> Sequence[GoogleAccount]:
        stmt = select(GoogleAccount).where(
            GoogleAccount.user_id == user_id, GoogleAccount.is_active == True
        ).order_by(GoogleAccount.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_spreadsheets(self, account_id: uuid.UUID) -> Sequence[Spreadsheet]:
        stmt = select(Spreadsheet).where(Spreadsheet.google_account_id == account_id).order_by(Spreadsheet.updated_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_sync_job(self, job_id: uuid.UUID) -> GoogleSyncJob | None:
        stmt = select(GoogleSyncJob).where(GoogleSyncJob.id == job_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def list_sync_history(self, limit: int = 50) -> Sequence[GoogleSyncHistory]:
        stmt = select(GoogleSyncHistory).order_by(GoogleSyncHistory.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_remapping_suggestions(self, validation_id: uuid.UUID) -> Sequence[RemappingSuggestion]:
        stmt = select(RemappingSuggestion).where(RemappingSuggestion.validation_id == validation_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
