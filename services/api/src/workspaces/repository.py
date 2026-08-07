import logging
from typing import Sequence
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.models import Invitation, Organization, Session, Team, Workspace

logger = logging.getLogger(__name__)


class WorkspaceRepository:
    """Repository handling persistence operations for Organization, Workspace, Team, Invitation, and Session."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_organizations(self) -> Sequence[Organization]:
        stmt = select(Organization).where(Organization.status != "archived").order_by(Organization.created_at.desc())
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
