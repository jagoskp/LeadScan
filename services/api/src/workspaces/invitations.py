import logging
from datetime import UTC, datetime, timedelta
import secrets
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.exceptions import InvitationExpiredException
from services.api.src.workspaces.models import Invitation
from services.api.src.workspaces.schemas import InvitationCreateSchema
from services.api.src.workspaces.validators import validate_role_name

logger = logging.getLogger(__name__)


class InvitationEngine:
    """Invitation Engine generating tokenized email invitations and managing acceptance/expiration."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_invitation(self, req: InvitationCreateSchema, valid_hours: int = 72) -> Invitation:
        validate_role_name(req.role_name)
        now = datetime.now(UTC)
        token = secrets.token_urlsafe(32)
        inv = Invitation(
            id=uuid.uuid4(),
            organization_id=req.organization_id,
            email=req.email,
            role_name=req.role_name,
            token=token,
            status="pending",
            expires_at=now + timedelta(hours=valid_hours),
            created_at=now,
        )
        self.db.add(inv)
        await self.db.commit()
        return inv

    async def accept_invitation(self, token: str) -> Invitation:
        stmt = select(Invitation).where(Invitation.token == token)
        res = await self.db.execute(stmt)
        inv = res.scalars().first()

        if not inv or inv.status != "pending":
            raise InvitationExpiredException(token)

        if datetime.now(UTC) > inv.expires_at:
            inv.status = "expired"
            await self.db.commit()
            raise InvitationExpiredException(token)

        inv.status = "accepted"
        await self.db.commit()
        return inv
