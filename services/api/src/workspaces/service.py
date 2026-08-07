import logging
from typing import Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.invitations import InvitationEngine
from services.api.src.workspaces.organization import OrganizationManager
from services.api.src.workspaces.permissions import RBACEngine
from services.api.src.workspaces.repository import WorkspaceRepository
from services.api.src.workspaces.schemas import (
    InvitationCreateSchema,
    InvitationSchema,
    OrganizationCreateSchema,
    OrganizationSchema,
    SessionSchema,
    TeamCreateSchema,
    TeamSchema,
    WorkspaceCreateSchema,
    WorkspaceSchema,
)
from services.api.src.workspaces.sessions import SessionManager
from services.api.src.workspaces.workspace import WorkspaceManager

logger = logging.getLogger(__name__)


class WorkspacePlatformService:
    """Facade Application Service for Enterprise Multi-Workspace Platform."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = WorkspaceRepository(db)
        self.org_manager = OrganizationManager(db)
        self.workspace_manager = WorkspaceManager(db)
        self.rbac_engine = RBACEngine(db)
        self.invitation_engine = InvitationEngine(db)
        self.session_manager = SessionManager(db)

    async def create_organization(self, req: OrganizationCreateSchema) -> OrganizationSchema:
        org = await self.org_manager.create_organization(req)
        return OrganizationSchema.model_validate(org)

    async def list_organizations(self) -> list[OrganizationSchema]:
        orgs = await self.repo.list_organizations()
        return [OrganizationSchema.model_validate(o) for o in orgs]

    async def create_workspace(self, req: WorkspaceCreateSchema) -> WorkspaceSchema:
        ws = await self.workspace_manager.create_workspace(req)
        return WorkspaceSchema.model_validate(ws)

    async def list_workspaces(self, org_id: uuid.UUID) -> list[WorkspaceSchema]:
        wss = await self.repo.list_workspaces(org_id)
        return [WorkspaceSchema.model_validate(w) for w in wss]

    async def invite_user(self, req: InvitationCreateSchema) -> InvitationSchema:
        inv = await self.invitation_engine.create_invitation(req)
        return InvitationSchema.model_validate(inv)

    async def accept_invitation(self, token: str) -> InvitationSchema:
        inv = await self.invitation_engine.accept_invitation(token)
        return InvitationSchema.model_validate(inv)

    async def list_invitations(self, org_id: uuid.UUID) -> list[InvitationSchema]:
        invs = await self.repo.list_invitations(org_id)
        return [InvitationSchema.model_validate(i) for i in invs]

    async def list_active_sessions(self, user_id: uuid.UUID) -> list[SessionSchema]:
        sessions = await self.session_manager.list_user_sessions(user_id)
        return [SessionSchema.model_validate(s) for s in sessions]

    async def force_logout_session(self, session_id: uuid.UUID) -> bool:
        return await self.session_manager.force_logout_session(session_id)
