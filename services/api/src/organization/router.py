import uuid
from typing import Any, Sequence
from fastapi import APIRouter, Depends, status
from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.organization.dependencies import get_organization_service
from services.api.src.organization.models import OrganizationMember
from services.api.src.organization.schemas import (
    ChangeRoleRequest,
    InviteMemberRequest,
    OrganizationCreate,
    OrganizationMemberResponse,
    OrganizationResponse,
    OrganizationUpdate,
)
from services.api.src.organization.service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organization-workspaces"])


def build_member_response(member: OrganizationMember) -> OrganizationMemberResponse:
    """Consolidate membership model and User credentials fields into output schema."""
    return OrganizationMemberResponse(
        id=member.id,
        organization_id=member.organization_id,
        user_id=member.user_id,
        role=member.role,
        created_at=member.created_at,
        username=member.user.username,
        email=member.user.email,
    )


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_org(
    data: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> Any:
    """Create a new organization workspace tenant."""
    return await org_service.create_organization(current_user, data)


@router.get("", response_model=list[OrganizationResponse])
async def list_my_orgs(
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> Any:
    """List all organization workspaces where the authenticated user is a member."""
    return await org_service.list_user_organizations(current_user.id)


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(
    org_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> Any:
    """Retrieve details for a specific organization workspace."""
    return await org_service.get_organization(current_user.id, org_id)


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_org(
    org_id: uuid.UUID,
    data: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> Any:
    """Update organization settings or details (requires Owner/Admin roles)."""
    return await org_service.update_organization(current_user.id, org_id, data)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_org(
    org_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> None:
    """Delete organization workspace tenant (requires Owner role)."""
    await org_service.delete_organization(current_user.id, org_id)


@router.get("/{org_id}/members", response_model=list[OrganizationMemberResponse])
async def list_org_members(
    org_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> Any:
    """List all members registered under the organization workspace."""
    members = await org_service.list_members(current_user.id, org_id)
    return [build_member_response(m) for m in members]


@router.post(
    "/{org_id}/members/invite",
    response_model=OrganizationMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def invite_member(
    org_id: uuid.UUID,
    data: InviteMemberRequest,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> Any:
    """Invite/add member user immediately to the organization workspace."""
    member = await org_service.invite_member(current_user.id, org_id, data)
    return build_member_response(member)


@router.delete("/{org_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    org_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> None:
    """Remove member from workspace (requires Owner/Admin; Owners cannot be deleted)."""
    await org_service.remove_member(current_user.id, org_id, user_id)


@router.patch("/{org_id}/members/{user_id}/role", response_model=OrganizationMemberResponse)
async def change_member_role(
    org_id: uuid.UUID,
    user_id: uuid.UUID,
    data: ChangeRoleRequest,
    current_user: User = Depends(get_current_user),
    org_service: OrganizationService = Depends(get_organization_service),
) -> Any:
    """Modify membership role for a user inside an organization workspace."""
    member = await org_service.change_member_role(
        current_user.id,
        org_id,
        user_id,
        data.role,
    )
    return build_member_response(member)
