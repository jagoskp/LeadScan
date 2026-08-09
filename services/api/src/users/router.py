from typing import Any
from fastapi import APIRouter, Depends, File, UploadFile, status
from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.users.dependencies import get_user_service
from services.api.src.users.schemas import (
    ChangePasswordRequest,
    UserProfileResponse,
    UserProfileUpdate,
)
from services.api.src.users.service import UserService

router = APIRouter(prefix="/users", tags=["user-management"])


def build_profile_response(user: User, profile: Any) -> UserProfileResponse:
    """Consolidate auth User and UserProfile data into a single output schema."""
    return UserProfileResponse(
        user_id=user.id,
        email=user.email,
        username=user.username,
        full_name=profile.full_name,
        phone=profile.phone,
        company=getattr(profile, "company", None),
        designation=getattr(profile, "designation", None),
        avatar_url=profile.avatar_url,
        preferences=profile.preferences,
        account_status=profile.account_status,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    """Retrieve profile data and preferences for the logged-in user."""
    profile = await user_service.get_or_create_profile(current_user)
    return build_profile_response(current_user, profile)


@router.put("/me/profile", response_model=UserProfileResponse)
async def update_my_profile_put(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    """Update profile and configurations (full replacement mapping)."""
    profile = await user_service.update_profile(current_user, data)
    return build_profile_response(current_user, profile)


@router.patch("/me/profile", response_model=UserProfileResponse)
async def update_my_profile_patch(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    """Update profile and configurations (partial patch mapping)."""
    profile = await user_service.update_profile(current_user, data)
    return build_profile_response(current_user, profile)


@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_my_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> None:
    """Modify user credentials, requiring verification of current password."""
    await user_service.change_password(current_user, data)


@router.post("/me/avatar", status_code=status.HTTP_201_CREATED)
async def upload_my_avatar(
    file: UploadFile = File(..., description="Image file to set as avatar"),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    """Upload user avatar file (API structure only, updates database path reference)."""
    url = await user_service.upload_avatar(current_user, file.filename or "avatar.png")
    return {"avatar_url": url}


@router.delete("/me/avatar", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_avatar(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> None:
    """Remove user avatar reference from database profile."""
    await user_service.delete_avatar(current_user)
