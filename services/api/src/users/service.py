import uuid
from services.api.src.auth.models import User
from services.api.src.auth.repository import UserRepository
from services.api.src.auth.security import hash_password, verify_password
from services.api.src.users.exceptions import (
    InvalidPasswordException,
    PasswordsMatchException,
    ProfileNotFoundException,
)
from services.api.src.users.models import UserProfile
from services.api.src.users.repository import UserProfileRepository
from services.api.src.users.schemas import ChangePasswordRequest, UserProfileUpdate


class UserService:
    """Service coordinating high-level User management logic."""

    def __init__(
        self,
        user_repo: UserRepository,
        profile_repo: UserProfileRepository,
    ) -> None:
        self.user_repo = user_repo
        self.profile_repo = profile_repo

    async def get_or_create_profile(self, user: User) -> UserProfile:
        """Fetch profile context. Creates default model if not persisted yet."""
        profile = await self.profile_repo.get_by_user_id(user.id)
        if not profile:
            profile = UserProfile(
                user_id=user.id,
                full_name=None,
                phone=None,
                avatar_url=None,
            )
            profile = await self.profile_repo.create(profile)
        return profile

    async def update_profile(self, user: User, data: UserProfileUpdate) -> UserProfile:
        """Update profile demographics and configurations."""
        # Ensure profile exists
        await self.get_or_create_profile(user)
        
        updated_profile = await self.profile_repo.update_profile(
            user_id=user.id,
            full_name=data.full_name,
            phone=data.phone,
            company=data.company,
            designation=data.designation,
            preferences=data.preferences,
        )
        if not updated_profile:
            raise ProfileNotFoundException()
        return updated_profile

    async def change_password(self, user: User, data: ChangePasswordRequest) -> None:
        """Verify current password, validate complexity rules and update credentials."""
        # Check current password match
        if not verify_password(data.current_password, user.hashed_password):
            raise InvalidPasswordException()

        # Ensure new password is not the same
        if verify_password(data.new_password, user.hashed_password):
            raise PasswordsMatchException()

        # Hash new password and save
        user.hashed_password = hash_password(data.new_password)
        await self.user_repo.create(user)

    async def upload_avatar(self, user: User, filename: str) -> str:
        """Simulate profile avatar uploading by saving file reference to database."""
        # Ensure profile exists
        await self.get_or_create_profile(user)

        # Build simulated URL storage reference
        simulated_url = f"/static/avatars/{user.id}_{filename}"
        await self.profile_repo.update_avatar_url(user.id, simulated_url)
        return simulated_url

    async def delete_avatar(self, user: User) -> None:
        """Delete profile avatar reference from database."""
        await self.get_or_create_profile(user)
        await self.profile_repo.update_avatar_url(user.id, None)
