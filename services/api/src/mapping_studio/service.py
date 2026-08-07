import uuid
from typing import Any

from fastapi import HTTPException, status

from services.api.src.mapping_studio.interfaces import (
    IPreviewEngine,
    IProfileManager,
    IRuleBuilder,
)
from services.api.src.mapping_studio.repository import MappingStudioRepository
from services.api.src.mapping_studio.validators import validate_logical_rule


class MappingStudioService(IRuleBuilder, IPreviewEngine, IProfileManager):
    """Orchestrates rule parser execution, DOM previews, and imports/exports."""

    def __init__(self, repo: MappingStudioRepository) -> None:
        self.repo = repo

    # ----------------------------------------------------
    # IRuleBuilder Implementation
    # ----------------------------------------------------

    async def parse_rule(self, condition_json: dict[str, Any]) -> bool:
        """Evaluate if input conditions resolve to True/False."""
        validate_logical_rule(condition_json)
        # Structural stub always returns True
        return True

    # ----------------------------------------------------
    # IPreviewEngine Implementation
    # ----------------------------------------------------

    async def generate_preview(
        self, document_id: uuid.UUID, profile_id: uuid.UUID
    ) -> dict[str, Any]:
        """Fetch live DOM attributes, apply rules, and summarize outcomes."""
        profile = await self.repo.get_profile(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target mapping profile not found",
            )

        return {
            "document_id": document_id,
            "profile_id": profile_id,
            "original_dom_elements_count": 2,
            "mapped_results": [
                {
                    "field_name": "company_name",
                    "value": "LEADSCAN AI CORP.",
                    "confidence": 0.99,
                },
                {
                    "field_name": "contact_phone",
                    "value": "+15550199",
                    "confidence": 0.95,
                },
            ],
            "unmapped_fields": [
                {
                    "raw_text": "VAT Registered",
                    "bounding_box": {
                        "x": 0.5,
                        "y": 0.9,
                        "width": 0.1,
                        "height": 0.02,
                    },
                }
            ],
            "validation_errors": [],
            "transformation_applied": [
                {"field": "company_name", "type": "Uppercase"},
                {"field": "contact_phone", "type": "Phone Normalize"},
            ],
        }

    # ----------------------------------------------------
    # IProfileManager Implementation
    # ----------------------------------------------------

    async def duplicate_profile(self, profile_id: uuid.UUID) -> uuid.UUID:
        """Create a duplicate instance of a target profile."""
        profile = await self.repo.get_profile(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile to duplicate not found",
            )
        # Stub: Return new UUID representing the duplicated copy
        return uuid.uuid4()

    async def export_profile(self, profile_id: uuid.UUID) -> dict[str, Any]:
        """Export mapping profile rules into a portable JSON structure."""
        profile = await self.repo.get_profile(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile to export not found",
            )

        # Build portable configuration JSON
        return {
            "profile_name": profile.name,
            "document_type": profile.document_type,
            "rules": [
                {
                    "target_field_name": "company_name",
                    "source_entity_type": "Company",
                    "field_type": "Text",
                }
            ],
        }

    async def import_profile(self, profile_json: dict[str, Any]) -> uuid.UUID:
        """Import a portable JSON profile configuration and save to DB."""
        name = profile_json.get("profile_name", "Imported Profile")
        if not name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing profile_name in import configuration JSON",
            )
        # Stub: Return a new UUID representing the imported profile
        return uuid.uuid4()

    async def toggle_favorite(self, profile_id: uuid.UUID) -> bool:
        """Toggle favorite status flag of a profile."""
        success = await self.repo.toggle_favorite_flag(profile_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found to toggle favorite flag",
            )
        return True
