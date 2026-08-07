import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.api.src.mapping.models import (
    MappedField,
    MappingHistory,
    MappingProfile,
    MappingRule,
    UnmappedField,
)


class MappingProfileRepository:
    """Repository handling persistence operations for MappingProfiles and rules."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, profile: MappingProfile) -> MappingProfile:
        """Persist a new MappingProfile configurations."""
        self.session.add(profile)
        await self.session.flush()
        return profile

    async def get_by_id(self, profile_id: uuid.UUID) -> MappingProfile | None:
        """Retrieve a specific MappingProfile preloading rules and targets."""
        stmt = (
            select(MappingProfile)
            .where(MappingProfile.id == profile_id)
            .options(
                selectinload(MappingProfile.rules).selectinload(
                    MappingRule.transformations
                ),
                selectinload(MappingProfile.rules).selectinload(
                    MappingRule.validations
                ),
                selectinload(MappingProfile.targets),
                selectinload(MappingProfile.history),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_profiles(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[MappingProfile]:
        """List MappingProfiles filtered by user context and organization."""
        stmt = select(MappingProfile).options(
            selectinload(MappingProfile.rules),
        )
        filters = []
        if user_id:
            filters.append(MappingProfile.user_id == user_id)
        if organization_id:
            filters.append(MappingProfile.organization_id == organization_id)
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(
        self, profile_id: uuid.UUID, data: dict[str, Any]
    ) -> MappingProfile | None:
        """Update profile properties."""
        if data:
            stmt = (
                update(MappingProfile)
                .where(MappingProfile.id == profile_id)
                .values(**data)
            )
            await self.session.execute(stmt)
        return await self.get_by_id(profile_id)

    async def delete(self, profile_id: uuid.UUID) -> bool:
        """Delete a MappingProfile configuration from the database."""
        stmt = delete(MappingProfile).where(MappingProfile.id == profile_id)
        result = await self.session.execute(stmt)
        return bool(getattr(result, "rowcount", 0))


class MappedFieldRepository:
    """Repository handling persistence operations for mapped outcomes."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_mapped_field(self, field: MappedField) -> MappedField:
        """Persist MappedField log."""
        self.session.add(field)
        await self.session.flush()
        return field

    async def get_mapped_fields_by_doc(
        self, doc_id: uuid.UUID
    ) -> Sequence[MappedField]:
        """Retrieve mapped fields associated with target DOM Document ID."""
        stmt = select(MappedField).where(MappedField.document_id == doc_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_unmapped_field(self, field: UnmappedField) -> UnmappedField:
        """Persist UnmappedField log to prevent data loss."""
        self.session.add(field)
        await self.session.flush()
        return field

    async def create_history(self, history: MappingHistory) -> MappingHistory:
        """Persist profile update histories logs."""
        self.session.add(history)
        await self.session.flush()
        return history
