import logging
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.interfaces import IRBACEngine
from services.api.src.workspaces.models import Membership, Permission, Role

logger = logging.getLogger(__name__)


class RBACEngine(IRBACEngine):
    """RBAC Permission Engine evaluating user capability grants (Owner, Admin, Manager, Operator, Reviewer, Viewer)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def verify_permission(self, user_id: uuid.UUID, org_id: uuid.UUID, action: str) -> bool:
        stmt = (
            select(Membership)
            .where(Membership.user_id == user_id, Membership.organization_id == org_id)
        )
        res = await self.db.execute(stmt)
        membership = res.scalars().first()

        if not membership:
            return False

        # Owner & Admin role bypass
        role = await self.db.get(Role, membership.role_id)
        if role and role.name in {"Owner", "Admin"}:
            return True

        # Check explicit permission grant
        stmt_perm = select(Permission).where(Permission.role_id == membership.role_id, Permission.action == action)
        res_perm = await self.db.execute(stmt_perm)
        return res_perm.scalars().first() is not None
