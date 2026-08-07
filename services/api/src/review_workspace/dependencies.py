# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.review_workspace.repository import (
    ReviewItemRepository,
    ReviewSessionRepository,
)
from services.api.src.review_workspace.service import ReviewWorkspaceService


def get_review_session_repository(
    session: AsyncSession = Depends(get_db),
) -> ReviewSessionRepository:
    """Inject ReviewSessionRepository context."""
    return ReviewSessionRepository(session)


def get_review_item_repository(
    session: AsyncSession = Depends(get_db),
) -> ReviewItemRepository:
    """Inject ReviewItemRepository context."""
    return ReviewItemRepository(session)


def get_review_workspace_service(
    session_repo: ReviewSessionRepository = Depends(
        get_review_session_repository
    ),
    item_repo: ReviewItemRepository = Depends(get_review_item_repository),
) -> ReviewWorkspaceService:
    """Inject ReviewWorkspaceService context."""
    return ReviewWorkspaceService(session_repo, item_repo)
