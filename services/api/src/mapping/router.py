# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.mapping.dependencies import get_mapping_engine_service
from services.api.src.mapping.schemas import (
    MappedFieldResponse,
    MappingHistoryResponse,
    MappingProfileCreate,
    MappingProfileResponse,
    MappingProfileUpdate,
)
from services.api.src.mapping.service import MappingEngineService

router = APIRouter(prefix="/mapping", tags=["mapping"])


# ----------------------------------------------------
# Mapping Profiles Endpoints
# ----------------------------------------------------

@router.post(
    "/profiles",
    response_model=MappingProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_mapping_profile(
    data: MappingProfileCreate,
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> Any:
    """Create a new mapping profile configuration."""
    return await service.create_profile(user_id=current_user.id, data=data)


@router.get("/profiles", response_model=list[MappingProfileResponse])
async def list_mapping_profiles(
    organization_id: uuid.UUID | None = Query(
        None, description="Filter by organization"
    ),
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> Any:
    """List mapping profiles filtered by user context and organization."""
    return await service.list_profiles(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/profiles/{profile_id}", response_model=MappingProfileResponse)
async def get_mapping_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> Any:
    """Retrieve detailed properties of a mapping profile configuration."""
    return await service.get_profile(profile_id)


@router.patch("/profiles/{profile_id}", response_model=MappingProfileResponse)
async def update_mapping_profile(
    profile_id: uuid.UUID,
    data: MappingProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> Any:
    """Update properties of a mapping profile configuration."""
    return await service.update_profile(
        profile_id=profile_id, author_id=current_user.id, data=data
    )


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mapping_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> None:
    """Delete a mapping profile configuration."""
    await service.delete_profile(profile_id)


# ----------------------------------------------------
# Mapping Execution Endpoints
# ----------------------------------------------------

@router.post("/execute")
async def execute_dynamic_mapping(
    document_id: uuid.UUID = Query(..., description="Target DOM Document ID"),
    profile_id: uuid.UUID = Query(..., description="Target Mapping Profile ID"),
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> Any:
    """Convert DOM Document fields according to Mapping Profile rules."""
    return await service.execute_mapping(document_id, profile_id)


@router.get("/history/{profile_id}", response_model=list[MappingHistoryResponse])
async def get_profile_history(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> Any:
    """Retrieve previous snapshot version logs of a target profile."""
    profile = await service.get_profile(profile_id)
    return profile.history


@router.get("/fields/{document_id}", response_model=list[MappedFieldResponse])
async def get_mapped_fields(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: MappingEngineService = Depends(get_mapping_engine_service),
) -> Any:
    """Retrieve previously mapped field values for a specific Document ID."""
    return await service.mapped_repo.get_mapped_fields_by_doc(document_id)
