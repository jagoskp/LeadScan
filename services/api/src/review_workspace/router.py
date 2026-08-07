# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.review_workspace.dependencies import (
    get_review_workspace_service,
)
from services.api.src.review_workspace.schemas import (
    ReviewItemUpdate,
    ReviewSessionCreate,
    ReviewSessionResponse,
)
from services.api.src.review_workspace.service import ReviewWorkspaceService

router = APIRouter(prefix="/review", tags=["review"])


# ----------------------------------------------------
# Review Session Endpoints
# ----------------------------------------------------

@router.post(
    "/sessions",
    response_model=ReviewSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review_session(
    payload: ReviewSessionCreate,
    current_user: User = Depends(get_current_user),
    service: ReviewWorkspaceService = Depends(get_review_workspace_service),
) -> Any:
    """Create a new review session linked to target DOM Document ID."""
    return await service.create_session(payload.document_id)


@router.get("/sessions", response_model=list[ReviewSessionResponse])
async def list_review_sessions(
    current_user: User = Depends(get_current_user),
    service: ReviewWorkspaceService = Depends(get_review_workspace_service),
) -> Any:
    """List review sessions."""
    return await service.list_active_sessions()


@router.get("/sessions/{session_id}")
async def get_review_session_details(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ReviewWorkspaceService = Depends(get_review_workspace_service),
) -> Any:
    """Retrieve detailed properties of a review session."""
    return await service.get_session_details(session_id)


@router.patch("/items/{item_id}")
async def correct_review_item(
    item_id: uuid.UUID,
    payload: ReviewItemUpdate,
    current_user: User = Depends(get_current_user),
    service: ReviewWorkspaceService = Depends(get_review_workspace_service),
) -> Any:
    """Apply manual edits to a review item value."""
    return await service.apply_manual_correction(
        item_id=item_id,
        corrector_id=current_user.id,
        new_value=payload.current_value,
        reason=payload.reason,
    )


@router.post("/sessions/{session_id}/approve")
async def approve_review_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: ReviewWorkspaceService = Depends(get_review_workspace_service),
) -> Any:
    """Submit final approval of the review session."""
    success = await service.submit_session_approval(
        session_id=session_id, reviewer_id=current_user.id
    )
    return {"success": success}
