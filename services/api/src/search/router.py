import logging
from typing import Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.search.exceptions import SearchException
from services.api.src.search.schemas import (
    AutocompleteSuggestionSchema,
    RecentSearchSchema,
    SavedSearchCreateSchema,
    SavedSearchSchema,
    UniversalSearchRequest,
    UniversalSearchResponse,
)
from services.api.src.search.service import SearchService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/search", tags=["Enterprise Universal Search Engine"])


@router.post("/universal", response_model=UniversalSearchResponse)
async def execute_universal_search(
    payload: UniversalSearchRequest,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """Global multi-entity search endpoint across Lead Repository, Contacts, Companies, Timeline, Notes, Tags, OCR, and AI."""
    try:
        service = SearchService(db)
        return await service.execute_universal_search(payload, user_id)
    except SearchException as exc:
        raise HTTPException(status_code=400, detail=exc.message)


@router.get("/suggestions", response_model=list[AutocompleteSuggestionSchema])
async def get_autocomplete_suggestions(
    prefix: str = Query(..., min_length=1),
    limit: int = Query(default=5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """Instant autocomplete suggestions for search bar."""
    service = SearchService(db)
    return await service.get_autocomplete_suggestions(prefix, limit)


@router.post("/saved-searches", response_model=SavedSearchSchema, status_code=status.HTTP_201_CREATED)
async def create_saved_search(
    payload: SavedSearchCreateSchema,
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """Save a search query and filter preset."""
    service = SearchService(db)
    return await service.save_search(user_id, payload)


@router.get("/saved-searches", response_model=list[SavedSearchSchema])
async def list_saved_searches(
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    db: AsyncSession = Depends(get_db),
):
    """List bookmarked saved searches."""
    service = SearchService(db)
    return await service.list_saved_searches(user_id)


@router.get("/recent", response_model=list[RecentSearchSchema])
async def list_recent_searches(
    user_id: uuid.UUID = Query(default_factory=uuid.uuid4),
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Get user's recent search query history."""
    service = SearchService(db)
    return await service.list_recent_searches(user_id, limit)
