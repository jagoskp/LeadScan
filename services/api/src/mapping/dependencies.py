# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.mapping.repository import (
    MappedFieldRepository,
    MappingProfileRepository,
)
from services.api.src.mapping.service import MappingEngineService


def get_mapping_profile_repository(
    session: AsyncSession = Depends(get_db),
) -> MappingProfileRepository:
    """Inject MappingProfileRepository context."""
    return MappingProfileRepository(session)


def get_mapped_field_repository(
    session: AsyncSession = Depends(get_db),
) -> MappedFieldRepository:
    """Inject MappedFieldRepository context."""
    return MappedFieldRepository(session)


def get_mapping_engine_service(
    profile_repo: MappingProfileRepository = Depends(
        get_mapping_profile_repository
    ),
    mapped_repo: MappedFieldRepository = Depends(
        get_mapped_field_repository
    ),
) -> MappingEngineService:
    """Inject MappingEngineService context."""
    return MappingEngineService(profile_repo, mapped_repo)
