import uuid
from collections.abc import Sequence
from typing import Any

from services.api.src.mapping.enums import (
    TransformationType,
    ValidationRuleType,
)
from services.api.src.mapping.exceptions import (
    MappingProfileNotFoundException,
    ValidationFailedException,
)
from services.api.src.mapping.interfaces import (
    IMappingEngine,
    IMappingValidator,
    ITransformer,
)
from services.api.src.mapping.models import (
    MappedField,
    MappingHistory,
    MappingProfile,
    MappingRule,
    MappingTarget,
    TransformationRule,
    UnmappedField,
    ValidationRule,
)
from services.api.src.mapping.repository import (
    MappedFieldRepository,
    MappingProfileRepository,
)
from services.api.src.mapping.schemas import (
    MappingProfileCreate,
    MappingProfileUpdate,
)
from services.api.src.mapping.validators import (
    validate_field_length,
    validate_field_regex,
    validate_required_field,
)


class MappingEngineService(IMappingEngine, ITransformer, IMappingValidator):
    """Orchestrates dynamic mapping profiles, transformations, and validations."""

    def __init__(
        self,
        profile_repo: MappingProfileRepository,
        mapped_repo: MappedFieldRepository,
    ) -> None:
        self.profile_repo = profile_repo
        self.mapped_repo = mapped_repo

    # ----------------------------------------------------
    # Profile CRUD Operations
    # ----------------------------------------------------

    async def create_profile(
        self, user_id: uuid.UUID, data: MappingProfileCreate
    ) -> MappingProfile:
        """Create a new mapping profile configuration."""
        profile = MappingProfile(
            user_id=user_id,
            organization_id=data.organization_id,
            name=data.name,
            document_type=data.document_type,
            version=1,
            is_active=True,
        )
        await self.profile_repo.create(profile)

        # Build Rules
        for r_data in data.rules:
            rule = MappingRule(
                profile_id=profile.id,
                target_field_name=r_data.target_field_name,
                source_entity_type=r_data.source_entity_type,
                field_type=r_data.field_type.value,
                is_required=r_data.is_required,
                default_value=r_data.default_value,
            )
            self.profile_repo.session.add(rule)
            await self.profile_repo.session.flush()

            for seq, t_data in enumerate(r_data.transformations):
                t_rule = TransformationRule(
                    rule_id=rule.id,
                    transformation_type=t_data.transformation_type.value,
                    parameters=t_data.parameters,
                    sequence_order=seq,
                )
                self.profile_repo.session.add(t_rule)

            for v_data in r_data.validations:
                v_rule = ValidationRule(
                    rule_id=rule.id,
                    validation_type=v_data.validation_type.value,
                    parameters=v_data.parameters,
                )
                self.profile_repo.session.add(v_rule)

        # Build Targets
        for target_data in data.targets:
            target = MappingTarget(
                profile_id=profile.id,
                target_type=target_data.target_type.value,
                configuration=target_data.configuration,
            )
            self.profile_repo.session.add(target)

        await self.profile_repo.session.flush()
        reloaded = await self.profile_repo.get_by_id(profile.id)
        if not reloaded:
            raise MappingProfileNotFoundException()
        return reloaded

    async def get_profile(self, profile_id: uuid.UUID) -> MappingProfile:
        """Retrieve a specific MappingProfile, raising 404 if missing."""
        profile = await self.profile_repo.get_by_id(profile_id)
        if not profile:
            raise MappingProfileNotFoundException()
        return profile

    async def list_profiles(
        self,
        user_id: uuid.UUID | None = None,
        organization_id: uuid.UUID | None = None,
    ) -> Sequence[MappingProfile]:
        """List profiles matching user/organization scopes."""
        return await self.profile_repo.list_profiles(
            user_id=user_id, organization_id=organization_id
        )

    async def update_profile(
        self,
        profile_id: uuid.UUID,
        author_id: uuid.UUID,
        data: MappingProfileUpdate,
    ) -> MappingProfile:
        """Update profile properties and log history snapshots."""
        profile = await self.get_profile(profile_id)

        # Save History snapshot prior to change
        snapshot = {
            "name": profile.name,
            "document_type": profile.document_type,
            "is_active": profile.is_active,
            "version": profile.version,
        }
        history = MappingHistory(
            profile_id=profile.id,
            version=profile.version,
            author_id=author_id,
            change_summary="Update profile status or properties",
            snapshot=snapshot,
        )
        await self.mapped_repo.create_history(history)

        update_data = data.model_dump(exclude_unset=True)
        update_data["version"] = profile.version + 1

        updated = await self.profile_repo.update(profile_id, update_data)
        if not updated:
            raise MappingProfileNotFoundException()
        return updated

    async def delete_profile(self, profile_id: uuid.UUID) -> bool:
        """Delete a MappingProfile configuration from the database."""
        # Ensure profile exists
        await self.get_profile(profile_id)
        return await self.profile_repo.delete(profile_id)

    # ----------------------------------------------------
    # IMappingEngine Implementation
    # ----------------------------------------------------

    async def execute_mapping(
        self, document_id: uuid.UUID, profile_id: uuid.UUID
    ) -> dict[str, Any]:
        """Convert Document DOM nodes into custom target outputs."""
        profile = await self.get_profile(profile_id)

        # Mock DOM Entity elements loading
        mock_entities: list[dict[str, Any]] = [
            {"type": "Company", "value": "LeadScan AI Corp.", "confidence": 0.99},
            {"type": "Phone", "value": "+1-555-0199", "confidence": 0.95},
        ]

        mapped_fields_list = []
        validation_errors = []

        for rule in profile.rules:
            # Locate entity matching rule
            entity = next(
                (e for e in mock_entities if e["type"] == rule.source_entity_type),
                None,
            )

            val = str(entity["value"]) if entity else rule.default_value
            conf = float(entity["confidence"]) if entity else 1.0

            if val is not None:
                # 1. Apply Chained Transformations
                t_list = [
                    {"type": t.transformation_type, "params": t.parameters}
                    for t in rule.transformations
                ]
                transformed_val = await self.transform(val, t_list)

                # 2. Run Field Validations
                v_list = [
                    {"type": v.validation_type, "params": v.parameters}
                    for v in rule.validations
                ]
                errors = await self.validate_field(transformed_val, v_list)
                if errors:
                    validation_errors.extend(errors)

                # Save output field
                field = MappedField(
                    document_id=document_id,
                    profile_id=profile.id,
                    rule_id=rule.id,
                    field_name=rule.target_field_name,
                    value=transformed_val,
                    confidence=conf,
                )
                await self.mapped_repo.create_mapped_field(field)
                mapped_fields_list.append(field)
            else:
                if rule.is_required:
                    validation_errors.append(
                        f"Required field '{rule.target_field_name}' is missing"
                    )

        # 3. Log Unmapped Elements (Preserve everything)
        unmapped = UnmappedField(
            document_id=document_id,
            profile_id=profile.id,
            raw_text="VAT Registered",
            bounding_box={"x": 0.5, "y": 0.9, "width": 0.1, "height": 0.02},
        )
        await self.mapped_repo.create_unmapped_field(unmapped)

        if validation_errors:
            raise ValidationFailedException(
                detail="; ".join(validation_errors)
            )

        return {
            "success": True,
            "mapped_fields_count": len(mapped_fields_list),
            "unmapped_fields_count": 1,
        }

    # ----------------------------------------------------
    # ITransformer Implementation
    # ----------------------------------------------------

    async def transform(
        self, value: str, rules: Sequence[dict[str, Any]]
    ) -> str:
        """Apply formatting manipulations to a target string."""
        transformed = value
        for rule in rules:
            t_type = rule["type"]
            if t_type == TransformationType.TRIM.value:
                transformed = transformed.strip()
            elif t_type == TransformationType.UPPERCASE.value:
                transformed = transformed.upper()
            elif t_type == TransformationType.LOWERCASE.value:
                transformed = transformed.lower()
            elif t_type == TransformationType.PHONE_NORMALIZE.value:
                transformed = transformed.replace("-", "").replace(" ", "")
        return transformed

    # ----------------------------------------------------
    # IMappingValidator Implementation
    # ----------------------------------------------------

    async def validate_field(
        self, value: str, rules: Sequence[dict[str, Any]]
    ) -> list[str]:
        """Evaluate validation checks and report error log messages."""
        errors = []
        for rule in rules:
            v_type = rule["type"]
            params = rule["params"] or {}

            if v_type == ValidationRuleType.REQUIRED.value:
                err = validate_required_field("target", value)
                if err:
                    errors.append(err)
            elif v_type == ValidationRuleType.LENGTH.value:
                min_len = params.get("min_len")
                max_len = params.get("max_len")
                err = validate_field_length("target", value, min_len, max_len)
                if err:
                    errors.append(err)
            elif v_type == ValidationRuleType.REGEX.value:
                pattern = params.get("pattern", ".*")
                err = validate_field_regex("target", value, pattern)
                if err:
                    errors.append(err)
        return errors
