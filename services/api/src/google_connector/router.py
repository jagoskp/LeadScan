import logging
from typing import Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.google_connector.exceptions import GoogleConnectorException
from services.api.src.google_connector.schemas import (
    ColumnDiscoveryResponse,
    GoogleAccountSchema,
    MappingValidationReportSchema,
    OAuthAuthUrlResponse,
    OAuthCallbackRequest,
    PreSyncCheckRequest,
    SyncExecutionRequest,
    SyncHistorySchema,
    SyncJobSchema,
)
from services.api.src.google_connector.service import GoogleConnectorService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/google-connector", tags=["Google Sheets Connector"])


@router.get("/oauth/auth-url", response_model=OAuthAuthUrlResponse)
async def get_oauth_auth_url(
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """Generate Google OAuth 2.0 authorization URL."""
    service = GoogleConnectorService(db)
    return await service.get_auth_url(user_id)


@router.post("/oauth/callback")
async def oauth_callback(
    payload: OAuthCallbackRequest,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """Handle OAuth callback code exchange."""
    try:
        service = GoogleConnectorService(db)
        return await service.handle_callback(user_id, payload.code, payload.redirect_uri)
    except GoogleConnectorException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/accounts", response_model=list[GoogleAccountSchema])
async def list_accounts(
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """List connected Google Accounts for user."""
    service = GoogleConnectorService(db)
    return await service.list_accounts(user_id)


@router.delete("/accounts/{account_id}")
async def disconnect_account(
    account_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Disconnect Google Account and revoke access tokens."""
    service = GoogleConnectorService(db)
    success = await service.oauth_service.disconnect_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account disconnected successfully"}


@router.get("/spreadsheets")
async def discover_spreadsheets(
    account_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Discover accessible Google Spreadsheets."""
    try:
        service = GoogleConnectorService(db)
        return await service.discover_spreadsheets(account_id)
    except GoogleConnectorException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/worksheets")
async def discover_worksheets(
    account_id: uuid.UUID = Query(...),
    spreadsheet_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Discover worksheets inside a spreadsheet."""
    try:
        service = GoogleConnectorService(db)
        return await service.discover_worksheets(account_id, spreadsheet_id)
    except GoogleConnectorException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/columns", response_model=ColumnDiscoveryResponse)
async def discover_columns(
    account_id: uuid.UUID = Query(...),
    spreadsheet_id: str = Query(...),
    worksheet_title: str = Query(default="Sheet1"),
    db: AsyncSession = Depends(get_db),
):
    """Dynamically discover column headers from Google Sheet."""
    try:
        service = GoogleConnectorService(db)
        return await service.discover_columns(account_id, spreadsheet_id, worksheet_title)
    except GoogleConnectorException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/pre-sync-check", response_model=MappingValidationReportSchema)
async def pre_sync_check(
    payload: PreSyncCheckRequest,
    account_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Validate dynamic mapping profile against live sheet columns before sync."""
    try:
        service = GoogleConnectorService(db)
        return await service.validate_pre_sync(
            profile_id=payload.profile_id,
            account_id=account_id,
            spreadsheet_id=payload.spreadsheet_id,
            worksheet_title=payload.worksheet_title,
        )
    except GoogleConnectorException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/sync", response_model=SyncJobSchema)
async def execute_sync(
    payload: SyncExecutionRequest,
    account_id: uuid.UUID = Query(...),
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """Execute real-time or batch synchronization to Google Sheet."""
    try:
        service = GoogleConnectorService(db)
        return await service.run_sync(account_id, payload, user_id)
    except GoogleConnectorException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/history", response_model=list[SyncHistorySchema])
async def get_sync_history(
    db: AsyncSession = Depends(get_db),
):
    """Get history log of synchronization executions."""
    service = GoogleConnectorService(db)
    return await service.get_sync_history()
