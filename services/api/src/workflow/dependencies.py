from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.ai.dependencies import get_ai_repository
from services.api.src.ai.repository import AIRepository
from services.api.src.database import get_db
from services.api.src.documents.dependencies import get_document_repository
from services.api.src.documents.repository import DocumentRepository
from services.api.src.ocr.dependencies import get_ocr_repository
from services.api.src.ocr.repository import OCRRepository
from services.api.src.organization.dependencies import (
    get_organization_member_repository,
)
from services.api.src.organization.repository import OrganizationMemberRepository
from services.api.src.workflow.repository import WorkflowRepository
from services.api.src.workflow.service import WorkflowService


def get_workflow_repository(
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> WorkflowRepository:
    """Inject WorkflowRepository context."""
    return WorkflowRepository(session)


def get_workflow_service(
    wf_repo: WorkflowRepository = Depends(get_workflow_repository),  # noqa: B008
    doc_repo: DocumentRepository = Depends(get_document_repository),  # noqa: B008
    ocr_repo: OCRRepository = Depends(get_ocr_repository),  # noqa: B008
    ai_repo: AIRepository = Depends(get_ai_repository),  # noqa: B008
    member_repo: OrganizationMemberRepository = Depends(  # noqa: B008
        get_organization_member_repository
    ),
) -> WorkflowService:
    """Inject WorkflowService context."""
    return WorkflowService(wf_repo, doc_repo, ocr_repo, ai_repo, member_repo)
