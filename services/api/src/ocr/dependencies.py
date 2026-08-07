from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.documents.dependencies import get_document_repository
from services.api.src.documents.repository import DocumentRepository
from services.api.src.ocr.repository import OCRRepository
from services.api.src.ocr.service import OCRService
from services.api.src.organization.dependencies import (
    get_organization_member_repository,
)
from services.api.src.organization.repository import OrganizationMemberRepository


def get_ocr_repository(
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> OCRRepository:
    """Inject OCRRepository context."""
    return OCRRepository(session)


def get_ocr_service(
    ocr_repo: OCRRepository = Depends(get_ocr_repository),  # noqa: B008
    doc_repo: DocumentRepository = Depends(get_document_repository),  # noqa: B008
    member_repo: OrganizationMemberRepository = Depends(  # noqa: B008
        get_organization_member_repository
    ),
) -> OCRService:
    """Inject OCRService context."""
    return OCRService(ocr_repo, doc_repo, member_repo)
