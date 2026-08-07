# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.mapping_studio.dependencies import (
    get_mapping_studio_service,
)
from services.api.src.mapping_studio.schemas import (
    PreviewRequest,
    PreviewResponse,
    ProfileExportResponse,
    ProfileImportRequest,
    RuleConditionSchema,
)
from services.api.src.mapping_studio.service import MappingStudioService

router = APIRouter(prefix="/mapping-studio", tags=["mapping_studio"])


# ----------------------------------------------------
# Logic Rule Builders
# ----------------------------------------------------

@router.post("/rules/validate")
async def validate_rule_condition(
    condition: RuleConditionSchema,
    current_user: User = Depends(get_current_user),
    service: MappingStudioService = Depends(get_mapping_studio_service),
) -> Any:
    """Validate format and logical condition keys."""
    success = await service.parse_rule(condition.model_dump())
    return {"success": success}


# ----------------------------------------------------
# DOM Live Preview Engine
# ----------------------------------------------------

@router.post("/preview", response_model=PreviewResponse)
async def generate_dom_preview(
    payload: PreviewRequest,
    current_user: User = Depends(get_current_user),
    service: MappingStudioService = Depends(get_mapping_studio_service),
) -> Any:
    """Acquire live DOM structures, apply rules, and summarize outcomes."""
    return await service.generate_preview(
        document_id=payload.document_id, profile_id=payload.profile_id
    )


# ----------------------------------------------------
# Profile Management
# ----------------------------------------------------

@router.post(
    "/profiles/{profile_id}/duplicate",
    status_code=status.HTTP_201_CREATED,
)
async def duplicate_mapping_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: MappingStudioService = Depends(get_mapping_studio_service),
) -> Any:
    """Duplicate a mapping profile configuration."""
    new_id = await service.duplicate_profile(profile_id)
    return {"duplicated_profile_id": new_id}


@router.post("/profiles/{profile_id}/export", response_model=ProfileExportResponse)
async def export_mapping_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: MappingStudioService = Depends(get_mapping_studio_service),
) -> Any:
    """Export profile rules configuration into JSON."""
    exported_json = await service.export_profile(profile_id)
    return ProfileExportResponse(profile_id=profile_id, exported_json=exported_json)


@router.post("/profiles/import", status_code=status.HTTP_201_CREATED)
async def import_mapping_profile(
    payload: ProfileImportRequest,
    current_user: User = Depends(get_current_user),
    service: MappingStudioService = Depends(get_mapping_studio_service),
) -> Any:
    """Import a portable JSON profile configuration into database."""
    new_id = await service.import_profile(payload.profile_json)
    return {"imported_profile_id": new_id}


@router.post("/profiles/{profile_id}/favorite")
async def toggle_favorite_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: MappingStudioService = Depends(get_mapping_studio_service),
) -> Any:
    """Toggle favorite status flag of a target profile."""
    success = await service.toggle_favorite(profile_id)
    return {"success": success}
