# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.document_model.repository import (
    DocumentRepository,
    EntityRepository,
)
from services.api.src.document_model.service import DOMEngineService


def get_dom_document_repository(
    session: AsyncSession = Depends(get_db),
) -> DocumentRepository:
    """Inject DocumentRepository context."""
    return DocumentRepository(session)


def get_dom_entity_repository(
    session: AsyncSession = Depends(get_db),
) -> EntityRepository:
    """Inject EntityRepository context."""
    return EntityRepository(session)


def get_dom_engine_service(
    doc_repo: DocumentRepository = Depends(get_dom_document_repository),
    entity_repo: EntityRepository = Depends(get_dom_entity_repository),
) -> DOMEngineService:
    """Inject DOMEngineService context."""
    return DOMEngineService(doc_repo, entity_repo)
