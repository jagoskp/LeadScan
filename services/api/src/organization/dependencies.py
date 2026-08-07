from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.database import get_db
from services.api.src.auth.dependencies import get_user_repository
from services.api.src.auth.repository import UserRepository
from services.api.src.organization.repository import (
    OrganizationMemberRepository,
    OrganizationRepository,
)
from services.api.src.organization.service import OrganizationService


def get_organization_repository(
    session: AsyncSession = Depends(get_db),
) -> OrganizationRepository:
    """Inject OrganizationRepository context."""
    return OrganizationRepository(session)


def get_organization_member_repository(
    session: AsyncSession = Depends(get_db),
) -> OrganizationMemberRepository:
    """Inject OrganizationMemberRepository context."""
    return OrganizationMemberRepository(session)


def get_organization_service(
    org_repo: OrganizationRepository = Depends(get_organization_repository),
    member_repo: OrganizationMemberRepository = Depends(get_organization_member_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> OrganizationService:
    """Inject OrganizationService context."""
    return OrganizationService(org_repo, member_repo, user_repo)
