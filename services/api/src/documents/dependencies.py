from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.documents.repository import DocumentRepository
from services.api.src.documents.service import DocumentService
from services.api.src.organization.dependencies import (
    get_organization_member_repository,
)
from services.api.src.organization.repository import OrganizationMemberRepository


def get_document_repository(
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> DocumentRepository:
    """Inject DocumentRepository context."""
    return DocumentRepository(session)


def get_document_service(
    doc_repo: DocumentRepository = Depends(get_document_repository),  # noqa: B008
    member_repo: OrganizationMemberRepository = Depends(  # noqa: B008
        get_organization_member_repository
    ),
) -> DocumentService:
    """Inject DocumentService context."""
    return DocumentService(doc_repo, member_repo)
