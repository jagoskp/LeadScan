import logging
from datetime import UTC, datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.models import Workspace
from services.api.src.workspaces.schemas import WorkspaceCreateSchema

logger = logging.getLogger(__name__)


class WorkspaceManager:
    """Workspace Manager managing isolated workspace environments under an Organization."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workspace(self, req: WorkspaceCreateSchema) -> Workspace:
        now = datetime.now(UTC)
        ws = Workspace(
            id=uuid.uuid4(),
            organization_id=req.organization_id,
            name=req.name,
            is_default=req.is_default,
            created_at=now,
        )
        self.db.add(ws)
        await self.db.commit()
        return ws
