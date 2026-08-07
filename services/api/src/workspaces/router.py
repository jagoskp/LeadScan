import logging
from typing import Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.workspaces.exceptions import WorkspacePlatformException
from services.api.src.workspaces.schemas import (
    InvitationCreateSchema,
    InvitationSchema,
    OrganizationCreateSchema,
    OrganizationSchema,
    SessionSchema,
    WorkspaceCreateSchema,
    WorkspaceSchema,
)
from services.api.src.workspaces.service import WorkspacePlatformService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/workspaces", tags=["Enterprise Multi-Workspace Platform"])


@router.get("/organizations", response_model=list[OrganizationSchema])
async def list_organizations(db: AsyncSession = Depends(get_db)):
    """List multi-tenant organizations."""
    service = WorkspacePlatformService(db)
    return await service.list_organizations()


@router.post("/organizations", response_model=OrganizationSchema, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create new multi-tenant organization account."""
    service = WorkspacePlatformService(db)
    return await service.create_organization(payload)


@router.get("", response_model=list[WorkspaceSchema])
async def list_workspaces(
    org_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """List isolated workspaces under an organization."""
    service = WorkspacePlatformService(db)
    return await service.list_workspaces(org_id)


@router.post("", response_model=WorkspaceSchema, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    payload: WorkspaceCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create new isolated workspace environment."""
    service = WorkspacePlatformService(db)
    return await service.create_workspace(payload)


@router.post("/invite", response_model=InvitationSchema, status_code=status.HTTP_201_CREATED)
async def invite_user(
    payload: InvitationCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Send tokenized email invitation to join organization."""
    try:
        service = WorkspacePlatformService(db)
        return await service.invite_user(payload)
    except WorkspacePlatformException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/accept-invitation", response_model=InvitationSchema)
async def accept_invitation(
    token: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Accept invitation using token."""
    try:
        service = WorkspacePlatformService(db)
        return await service.accept_invitation(token)
    except WorkspacePlatformException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/sessions", response_model=list[SessionSchema])
async def list_active_sessions(
    user_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """List active login sessions for user."""
    service = WorkspacePlatformService(db)
    return await service.list_active_sessions(user_id)


@router.post("/sessions/{session_id}/logout")
async def force_logout_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Force logout a user session."""
    service = WorkspacePlatformService(db)
    success = await service.force_logout_session(session_id)
    return {"success": success, "message": "Session terminated"}
