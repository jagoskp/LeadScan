import uuid
from typing import Sequence, Any
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.auth.models import User
from services.api.src.organization.models import Organization, OrganizationMember


class OrganizationRepository:
    """Repository managing Organization database operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, org_id: uuid.UUID) -> Organization | None:
        """Fetch organization by primary key."""
        result = await self.session.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Organization | None:
        """Fetch organization by unique slug."""
        result = await self.session.execute(
            select(Organization).where(Organization.slug == slug.lower())
        )
        return result.scalar_one_or_none()

    async def create(self, org: Organization) -> Organization:
        """Persist a new Organization model instance."""
        org.slug = org.slug.lower()
        self.session.add(org)
        await self.session.flush()
        return org

    async def update_org(
        self,
        org_id: uuid.UUID,
        name: str | None = None,
        slug: str | None = None,
        description: str | None = None,
        settings: dict[str, Any] | None = None,
    ) -> Organization | None:
        """Modify fields on an existing Organization."""
        update_data: dict[str, Any] = {}
        if name is not None:
            update_data["name"] = name
        if slug is not None:
            update_data["slug"] = slug.lower()
        if description is not None:
            update_data["description"] = description
        if settings is not None:
            update_data["settings"] = settings

        if update_data:
            await self.session.execute(
                update(Organization)
                .where(Organization.id == org_id)
                .values(**update_data)
            )
        return await self.get_by_id(org_id)

    async def delete_org(self, org_id: uuid.UUID) -> None:
        """Delete an Organization by ID."""
        await self.session.execute(
            delete(Organization).where(Organization.id == org_id)
        )


class OrganizationMemberRepository:
    """Repository managing OrganizationMember database operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_member(self, org_id: uuid.UUID, user_id: uuid.UUID) -> OrganizationMember | None:
        """Fetch simple membership mapping between user and organization."""
        result = await self.session.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == org_id,
                OrganizationMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_member_with_user(self, org_id: uuid.UUID, user_id: uuid.UUID) -> OrganizationMember | None:
        """Fetch member profile pre-loading User details to avoid lazy loading N+1 errors."""
        result = await self.session.execute(
            select(OrganizationMember)
            .options(joinedload(OrganizationMember.user))
            .where(
                OrganizationMember.organization_id == org_id,
                OrganizationMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_members_with_user(self, org_id: uuid.UUID) -> Sequence[OrganizationMember]:
        """List all members associated with an organization, loading user profiles."""
        result = await self.session.execute(
            select(OrganizationMember)
            .options(joinedload(OrganizationMember.user))
            .where(OrganizationMember.organization_id == org_id)
        )
        return result.scalars().all()

    async def list_user_memberships(self, user_id: uuid.UUID) -> Sequence[OrganizationMember]:
        """Fetch all organization memberships active for a user."""
        result = await self.session.execute(
            select(OrganizationMember)
            .options(joinedload(OrganizationMember.organization))
            .where(OrganizationMember.user_id == user_id)
        )
        return result.scalars().all()

    async def create(self, member: OrganizationMember) -> OrganizationMember:
        """Add user membership registration."""
        self.session.add(member)
        await self.session.flush()
        return member

    async def update_role(self, member_id: uuid.UUID, role: str) -> OrganizationMember | None:
        """Update role authority parameter for a member."""
        await self.session.execute(
            update(OrganizationMember)
            .where(OrganizationMember.id == member_id)
            .values(role=role)
        )
        # Fetch fresh with user preloaded
        result = await self.session.execute(
            select(OrganizationMember)
            .options(joinedload(OrganizationMember.user))
            .where(OrganizationMember.id == member_id)
        )
        return result.scalar_one_or_none()

    async def delete_member(self, member_id: uuid.UUID) -> None:
        """Remove a member registration."""
        await self.session.execute(
            delete(OrganizationMember).where(OrganizationMember.id == member_id)
        )
