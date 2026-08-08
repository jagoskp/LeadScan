import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.models import Invitation, Session, Team, TenantOrganization, Workspace

logger = logging.getLogger(__name__)


class WorkspaceRepository:
    """Repository handling persistence operations for TenantOrganization, Workspace, Team, Invitation, and Session."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_organizations(self) -> Sequence[TenantOrganization]:
        stmt = select(TenantOrganization).where(TenantOrganization.status != "archived").order_by(TenantOrganization.created_at.desc())
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def list_workspaces(self, org_id: uuid.UUID) -> Sequence[Workspace]:
        stmt = select(Workspace).where(Workspace.organization_id == org_id)
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def list_teams(self, workspace_id: uuid.UUID) -> Sequence[Team]:
        stmt = select(Team).where(Team.workspace_id == workspace_id)
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def list_invitations(self, org_id: uuid.UUID) -> Sequence[Invitation]:
        stmt = select(Invitation).where(Invitation.organization_id == org_id)
        res = await self.db.execute(stmt)
        return res.scalars().all()
