from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.src.database import get_db
from services.api.src.auth.dependencies import get_user_repository
from services.api.src.auth.repository import UserRepository
from services.api.src.users.repository import UserProfileRepository
from services.api.src.users.service import UserService


def get_user_profile_repository(
    session: AsyncSession = Depends(get_db),
) -> UserProfileRepository:
    """Inject UserProfileRepository context."""
    return UserProfileRepository(session)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    profile_repo: UserProfileRepository = Depends(get_user_profile_repository),
) -> UserService:
    """Inject UserService context."""
    return UserService(user_repo, profile_repo)
