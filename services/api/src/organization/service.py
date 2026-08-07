import uuid
from typing import Sequence
from services.api.src.auth.models import User
from services.api.src.auth.repository import UserRepository
from services.api.src.organization.exceptions import (
    ForbiddenOrganizationActionException,
    MemberAlreadyExistsException,
    MemberNotFoundException,
    OrganizationNotFoundException,
    SlugAlreadyExistsException,
)
from services.api.src.organization.models import Organization, OrganizationMember
from services.api.src.organization.repository import (
    OrganizationMemberRepository,
    OrganizationRepository,
)
from services.api.src.users.exceptions import ProfileNotFoundException
from services.api.src.organization.schemas import (
    InviteMemberRequest,
    OrganizationCreate,
    OrganizationUpdate,
)


class OrganizationService:
    """Service coordinates organization workspaces, settings and memberships."""

    def __init__(
        self,
        org_repo: OrganizationRepository,
        member_repo: OrganizationMemberRepository,
        user_repo: UserRepository,
    ) -> None:
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.user_repo = user_repo

    async def _check_privilege(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        required_roles: set[str],
    ) -> OrganizationMember:
        """Validate user membership and authority levels. Raises Forbidden if checks fail."""
        member = await self.member_repo.get_member(org_id, user_id)
        if not member or member.role not in required_roles:
            raise ForbiddenOrganizationActionException()
        return member

    async def create_organization(self, user: User, data: OrganizationCreate) -> Organization:
        """Create a new Organization tenant workspace and register creator as Owner."""
        # Verify slug uniqueness
        if await self.org_repo.get_by_slug(data.slug):
            raise SlugAlreadyExistsException()

        new_org = Organization(
            name=data.name,
            slug=data.slug,
            description=data.description,
            settings=data.settings or {"allow_invites": True, "timezone": "UTC"},
        )
        org = await self.org_repo.create(new_org)

        # Register membership creator as Owner
        creator_member = OrganizationMember(
            organization_id=org.id,
            user_id=user.id,
            role="Owner",
        )
        await self.member_repo.create(creator_member)

        return org

    async def get_organization(self, user_id: uuid.UUID, org_id: uuid.UUID) -> Organization:
        """Fetch organization if the requesting user is a member."""
        await self._check_privilege(org_id, user_id, {"Owner", "Admin", "Member"})
        org = await self.org_repo.get_by_id(org_id)
        if not org:
            raise OrganizationNotFoundException()
        return org

    async def list_user_organizations(self, user_id: uuid.UUID) -> Sequence[Organization]:
        """List all organization workspaces the user belongs to."""
        memberships = await self.member_repo.list_user_memberships(user_id)
        return [m.organization for m in memberships]

    async def update_organization(
        self,
        user_id: uuid.UUID,
        org_id: uuid.UUID,
        data: OrganizationUpdate,
    ) -> Organization:
        """Modify workspace parameters. Requires Admin or Owner access levels."""
        await self._check_privilege(org_id, user_id, {"Owner", "Admin"})

        # Check slug uniqueness if updated
        if data.slug:
            existing = await self.org_repo.get_by_slug(data.slug)
            if existing and existing.id != org_id:
                raise SlugAlreadyExistsException()

        updated = await self.org_repo.update_org(
            org_id=org_id,
            name=data.name,
            slug=data.slug,
            description=data.description,
            settings=data.settings,
        )
        if not updated:
            raise OrganizationNotFoundException()
        return updated

    async def delete_organization(self, user_id: uuid.UUID, org_id: uuid.UUID) -> None:
        """Remove organization workspace. Requires Owner privilege."""
        await self._check_privilege(org_id, user_id, {"Owner"})
        await self.org_repo.delete_org(org_id)

    async def invite_member(
        self,
        admin_id: uuid.UUID,
        org_id: uuid.UUID,
        data: InviteMemberRequest,
    ) -> OrganizationMember:
        """Invite/Add user immediately to the organization. Requires Admin or Owner roles."""
        await self._check_privilege(org_id, admin_id, {"Owner", "Admin"})

        # Retrieve target user to add
        target_user = await self.user_repo.get_by_email(data.email)
        if not target_user:
            raise ProfileNotFoundException()  # Simulates user lookup

        # Check existing membership
        if await self.member_repo.get_member(org_id, target_user.id):
            raise MemberAlreadyExistsException()

        new_member = OrganizationMember(
            organization_id=org_id,
            user_id=target_user.id,
            role=data.role,
        )
        await self.member_repo.create(new_member)

        # Retrieve preloaded User context
        member_with_user = await self.member_repo.get_member_with_user(org_id, target_user.id)
        if not member_with_user:
            raise MemberNotFoundException()
        return member_with_user

    async def remove_member(
        self,
        admin_id: uuid.UUID,
        org_id: uuid.UUID,
        user_to_remove: uuid.UUID,
    ) -> None:
        """Remove member from workspace. Owner cannot be removed; requires Admin or Owner."""
        admin_membership = await self._check_privilege(org_id, admin_id, {"Owner", "Admin"})
        
        target_membership = await self.member_repo.get_member(org_id, user_to_remove)
        if not target_membership:
            raise MemberNotFoundException()

        # Security checks
        if target_membership.role == "Owner":
            raise ForbiddenOrganizationActionException("Cannot remove the Owner of the organization")
        
        if admin_membership.role == "Admin" and target_membership.role == "Admin" and admin_id != user_to_remove:
            raise ForbiddenOrganizationActionException("Admins cannot remove other Admins")

        await self.member_repo.delete_member(target_membership.id)

    async def change_member_role(
        self,
        admin_id: uuid.UUID,
        org_id: uuid.UUID,
        user_to_update: uuid.UUID,
        new_role: str,
    ) -> OrganizationMember:
        """Modify membership role. Requires Admin/Owner; Owner role cannot be reassigned."""
        admin_membership = await self._check_privilege(org_id, admin_id, {"Owner", "Admin"})
        
        target_membership = await self.member_repo.get_member(org_id, user_to_update)
        if not target_membership:
            raise MemberNotFoundException()

        if target_membership.role == "Owner":
            raise ForbiddenOrganizationActionException("Owner role cannot be modified")
        
        if admin_membership.role == "Admin" and target_membership.role == "Admin" and admin_id != user_to_update:
            raise ForbiddenOrganizationActionException("Admins cannot modify roles of other Admins")

        updated = await self.member_repo.update_role(target_membership.id, new_role)
        if not updated:
            raise MemberNotFoundException()
        return updated

    async def list_members(self, user_id: uuid.UUID, org_id: uuid.UUID) -> Sequence[OrganizationMember]:
        """List all members registered under the organization. Requires active membership."""
        await self._check_privilege(org_id, user_id, {"Owner", "Admin", "Member"})
        return await self.member_repo.list_members_with_user(org_id)
