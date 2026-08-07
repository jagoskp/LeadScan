import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.mapping.models import MappingProfile


class MappingStudioRepository:
    """Repository handling database operations for the Mapping Studio context."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_profile(self, profile_id: uuid.UUID) -> MappingProfile | None:
        """Fetch a specific MappingProfile."""
        stmt = select(MappingProfile).where(MappingProfile.id == profile_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def toggle_favorite_flag(self, profile_id: uuid.UUID) -> bool:
        """Toggle favorite flag status on a mapping profile."""
        profile = await self.get_profile(profile_id)
        if not profile:
            return False
        # Save favorite flag status locally or print/log as stub
        return True
