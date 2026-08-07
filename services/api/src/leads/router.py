import logging
from typing import Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.leads.dependencies import get_lead_service
from services.api.src.leads.exceptions import LeadRepositoryException
from services.api.src.leads.schemas import (
    LeadCreateSchema,
    LeadMergeRequestSchema,
    LeadSchema,
    LeadTimelineSchema,
    LeadUpdateSchema,
)
from services.api.src.leads.service import LeadService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/leads", tags=["Enterprise Lead Repository"])


@router.get("", response_model=list[LeadSchema])
async def list_leads(
    search: str | None = Query(default=None, description="Search query across leads, contacts, company, GST"),
    status: str | None = Query(default=None, description="Filter by Lead status"),
    is_archived: bool = Query(default=False, description="Filter archived leads"),
    limit: int = Query(default=50, ge=1, le=200),
    service: LeadService = Depends(get_lead_service),
):
    """Search and list leads from the Enterprise Lead Repository."""
    return await service.list_leads(search_query=search, status=status, is_archived=is_archived, limit=limit)


@router.post("", response_model=LeadSchema, status_code=status.HTTP_201_CREATED)
async def create_lead(
    payload: LeadCreateSchema,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    service: LeadService = Depends(get_lead_service),
):
    """Create a new Master Lead record with company, contacts, and metadata lineage."""
    try:
        return await service.create_lead(payload, actor_id=user_id)
    except LeadRepositoryException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/{lead_id}", response_model=LeadSchema)
async def get_lead(
    lead_id: uuid.UUID,
    service: LeadService = Depends(get_lead_service),
):
    """Get single Lead record details with full lineage metadata."""
    try:
        return await service.get_lead(lead_id)
    except LeadRepositoryException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.patch("/{lead_id}", response_model=LeadSchema)
async def update_lead(
    lead_id: uuid.UUID,
    payload: LeadUpdateSchema,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    service: LeadService = Depends(get_lead_service),
):
    """Update Lead fields (title, status, priority, score, favorite)."""
    try:
        return await service.update_lead(lead_id, payload, actor_id=user_id)
    except LeadRepositoryException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/{lead_id}/archive", response_model=LeadSchema)
async def archive_lead(
    lead_id: uuid.UUID,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    service: LeadService = Depends(get_lead_service),
):
    """Soft-archive a Lead record."""
    try:
        return await service.archive_lead(lead_id, actor_id=user_id)
    except LeadRepositoryException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/{lead_id}/restore", response_model=LeadSchema)
async def restore_lead(
    lead_id: uuid.UUID,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    service: LeadService = Depends(get_lead_service),
):
    """Restore a soft-archived Lead record."""
    try:
        return await service.restore_lead(lead_id, actor_id=user_id)
    except LeadRepositoryException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/merge", response_model=LeadSchema)
async def merge_leads(
    payload: LeadMergeRequestSchema,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    service: LeadService = Depends(get_lead_service),
):
    """Merge secondary duplicate leads into a primary Lead record."""
    try:
        return await service.merge_leads(payload, actor_id=user_id)
    except LeadRepositoryException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/{lead_id}/timeline", response_model=list[LeadTimelineSchema])
async def get_lead_timeline(
    lead_id: uuid.UUID,
    service: LeadService = Depends(get_lead_service),
):
    """Get immutable event audit timeline for a Lead record."""
    return await service.get_timeline(lead_id)
