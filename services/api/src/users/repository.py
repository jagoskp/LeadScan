import uuid
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.users.models import UserProfile


class UserProfileRepository:
    """Repository managing UserProfile database persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(self, user_id: uuid.UUID) -> UserProfile | None:
        """Fetch a UserProfile record by the user ID key."""
        result = await self.session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, profile: UserProfile) -> UserProfile:
        """Persist a new UserProfile model instance."""
        self.session.add(profile)
        await self.session.flush()
        return profile

    async def update_profile(
        self,
        user_id: uuid.UUID,
        full_name: str | None = None,
        phone: str | None = None,
        preferences: dict | None = None,
    ) -> UserProfile | None:
        """Update profile fields on an existing record."""
        update_data: dict[str, Any] = {}
        if full_name is not None:
            update_data["full_name"] = full_name
        if phone is not None:
            update_data["phone"] = phone
        if preferences is not None:
            update_data["preferences"] = preferences

        if update_data:
            await self.session.execute(
                update(UserProfile)
                .where(UserProfile.user_id == user_id)
                .values(**update_data)
            )
        return await self.get_by_user_id(user_id)

    async def update_avatar_url(self, user_id: uuid.UUID, avatar_url: str | None) -> None:
        """Update or delete the avatar URL reference for a user."""
        await self.session.execute(
            update(UserProfile)
            .where(UserProfile.user_id == user_id)
            .values(avatar_url=avatar_url)
        )
