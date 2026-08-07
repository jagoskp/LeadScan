import logging
from datetime import UTC, datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.workspaces.models import Organization
from services.api.src.workspaces.schemas import OrganizationCreateSchema

logger = logging.getLogger(__name__)


class OrganizationManager:
    """Organization Manager handling multi-tenant account lifecycle (Create, Update, Suspend, Soft Delete)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_organization(self, req: OrganizationCreateSchema) -> Organization:
        now = datetime.now(UTC)
        org = Organization(
            id=uuid.uuid4(),
            name=req.name,
            logo_url=req.logo_url,
            timezone=req.timezone,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.add(org)
        await self.db.commit()
        return org

    async def suspend_organization(self, org_id: uuid.UUID) -> Organization:
        org = await self.db.get(Organization, org_id)
        if not org:
            raise ValueError("Organization not found")
        org.status = "suspended"
        org.updated_at = datetime.now(UTC)
        await self.db.commit()
        return org
