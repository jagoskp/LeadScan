import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import select

from services.api.src.ai.exceptions import (
    AIJobNotCancellableException,
    AIJobNotFoundException,
    AIJobNotRetriableException,
    OCRResultNotFoundException,
)
from services.api.src.ai.models import AIJob
from services.api.src.ai.repository import AIRepository
from services.api.src.ai.schemas import AIJobCreate
from services.api.src.documents.exceptions import DocumentNotFoundException
from services.api.src.documents.repository import DocumentRepository
from services.api.src.ocr.models import OCRResult
from services.api.src.ocr.repository import OCRRepository
from services.api.src.organization.exceptions import (
    ForbiddenOrganizationActionException,
)
from services.api.src.organization.repository import OrganizationMemberRepository


class AIService:
    """Service coordinates AI Analysis job lifecycles and tenancy checks."""

    def __init__(
        self,
        ai_repo: AIRepository,
        doc_repo: DocumentRepository,
        ocr_repo: OCRRepository,
        member_repo: OrganizationMemberRepository,
    ) -> None:
        self.ai_repo = ai_repo
        self.doc_repo = doc_repo
        self.ocr_repo = ocr_repo
        self.member_repo = member_repo

    async def _verify_org_membership(
        self, org_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """Validate user membership inside organization."""
        member = await self.member_repo.get_member(org_id, user_id)
        if not member:
            raise ForbiddenOrganizationActionException()

    async def create_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        data: AIJobCreate,
    ) -> AIJob:
        """Create new AI Job after validating document and OCR results."""
        await self._verify_org_membership(org_id, user_id)

        # Validate document exists and belongs to the organization
        document = await self.doc_repo.get_by_id_and_org(data.document_id, org_id)
        if not document:
            raise DocumentNotFoundException()

        # Validate OCR result exists, belongs to org and matches document
        ocr_res = await self.ocr_repo.session.execute(
            select(OCRResult).where(
                OCRResult.id == data.ocr_result_id,
                OCRResult.organization_id == org_id,
                OCRResult.document_id == data.document_id,
            )
        )
        ocr_result = ocr_res.scalar_one_or_none()
        if not ocr_result:
            raise OCRResultNotFoundException()

        job = AIJob(
            document_id=data.document_id,
            ocr_result_id=data.ocr_result_id,
            organization_id=org_id,
            owner_id=user_id,
            provider=data.provider,
            model_name=data.model_name,
            prompt_version=data.prompt_version,
            status="PENDING",
        )
        return await self.ai_repo.create_job(job)

    async def get_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> AIJob:
        """Retrieve details of specific AI job. Validates org access."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ai_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise AIJobNotFoundException()
        return job

    async def list_jobs(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        status: str | None = None,
        provider: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AIJob]:
        """List AI jobs in organization. Validates org access."""
        await self._verify_org_membership(org_id, user_id)
        return await self.ai_repo.list_jobs_by_org(
            org_id, status=status, provider=provider, skip=skip, limit=limit
        )

    async def delete_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> None:
        """Permanently delete AI job. Validates org access."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ai_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise AIJobNotFoundException()

        await self.ai_repo.delete_job(job_id)

    async def cancel_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> AIJob:
        """Cancel pending, queued, or running AI job."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ai_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise AIJobNotFoundException()

        cancellable = {"PENDING", "QUEUED", "RUNNING"}
        if job.status not in cancellable:
            raise AIJobNotCancellableException()

        update_dict = {
            "status": "CANCELLED",
            "updated_at": datetime.now(UTC),
        }
        updated = await self.ai_repo.update_job(job_id, update_dict)
        if not updated:
            raise AIJobNotFoundException()
        return updated

    async def retry_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> AIJob:
        """Retry failed or cancelled AI job."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ai_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise AIJobNotFoundException()

        retriable = {"FAILED", "CANCELLED"}
        if job.status not in retriable:
            raise AIJobNotRetriableException()

        # Delete any associated previous result before resetting
        await self.ai_repo.delete_result_by_job_id(job_id)

        update_dict = {
            "status": "PENDING",
            "updated_at": datetime.now(UTC),
        }
        updated = await self.ai_repo.update_job(job_id, update_dict)
        if not updated:
            raise AIJobNotFoundException()
        return updated
