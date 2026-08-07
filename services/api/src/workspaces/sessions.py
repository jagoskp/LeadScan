import logging
from datetime import UTC, datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.interfaces import ISessionManager
from services.api.src.workspaces.models import Session

logger = logging.getLogger(__name__)


class SessionManager(ISessionManager):
    """Session Manager handling active login sessions, device tracking, and force logout."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_user_sessions(self, user_id: uuid.UUID) -> list[Session]:
        stmt = select(Session).where(Session.user_id == user_id, Session.is_active.is_(True))
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def force_logout_session(self, session_id: uuid.UUID) -> bool:
        sess = await self.db.get(Session, session_id)
        if not sess:
            return False
        sess.is_active = False
        await self.db.commit()
        return True
