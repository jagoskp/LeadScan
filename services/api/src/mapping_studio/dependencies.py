# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.mapping_studio.repository import MappingStudioRepository
from services.api.src.mapping_studio.service import MappingStudioService


def get_mapping_studio_repository(
    session: AsyncSession = Depends(get_db),
) -> MappingStudioRepository:
    """Inject MappingStudioRepository context."""
    return MappingStudioRepository(session)


def get_mapping_studio_service(
    repo: MappingStudioRepository = Depends(get_mapping_studio_repository),
) -> MappingStudioService:
    """Inject MappingStudioService context."""
    return MappingStudioService(repo)
