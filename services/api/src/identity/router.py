import logging
from typing import Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.identity.exceptions import IdentityResolutionException
from services.api.src.identity.schemas import (
    DuplicateMatchSchema,
    MergeExecuteRequest,
    MergeHistorySchema,
    MergePreviewResponse,
    RollbackHistorySchema,
)
from services.api.src.identity.service import IdentityService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/identity", tags=["Enterprise Identity Resolution & Smart Duplicate Engine"])


@router.get("/duplicates", response_model=list[DuplicateMatchSchema])
async def list_duplicate_matches(
    status_filter: str = Query(default="pending", alias="status"),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List detected potential duplicate match pairs."""
    service = IdentityService(db)
    return await service.list_duplicate_matches(status=status_filter, limit=limit)


@router.post("/scan", response_model=list[DuplicateMatchSchema])
async def scan_for_duplicates(
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Trigger background duplicate scanning across active Master Lead records."""
    service = IdentityService(db)
    return await service.scan_for_duplicates(limit=limit)


@router.get("/merge-preview", response_model=MergePreviewResponse)
async def get_merge_preview(
    primary_lead_id: uuid.UUID = Query(...),
    secondary_lead_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Preview field differences and conflicts before merging leads."""
    try:
        service = IdentityService(db)
        return await service.get_merge_preview(primary_lead_id, secondary_lead_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/merge", response_model=MergeHistorySchema, status_code=status.HTTP_201_CREATED)
async def execute_merge(
    payload: MergeExecuteRequest,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """Safely merge secondary duplicate leads into a primary lead with full rollback snapshotting."""
    try:
        service = IdentityService(db)
        return await service.execute_merge(payload, actor_id=user_id)
    except IdentityResolutionException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/rollback/{merge_history_id}", response_model=RollbackHistorySchema)
async def rollback_merge(
    merge_history_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Rollback a previously executed merge operation and un-archive secondary lead."""
    try:
        service = IdentityService(db)
        return await service.rollback_merge(merge_history_id)
    except IdentityResolutionException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
