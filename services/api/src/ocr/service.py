import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

from services.api.src.documents.exceptions import DocumentNotFoundException
from services.api.src.documents.repository import DocumentRepository
from services.api.src.ocr.exceptions import (
    OCRJobNotCancellableException,
    OCRJobNotFoundException,
    OCRJobNotRetriableException,
)
from services.api.src.ocr.models import OCRJob
from services.api.src.ocr.repository import OCRRepository
from services.api.src.ocr.schemas import OCRJobCreate
from services.api.src.organization.exceptions import (
    ForbiddenOrganizationActionException,
)
from services.api.src.organization.repository import OrganizationMemberRepository


class OCRService:
    """Service coordinating OCR jobs management and lifecycle."""

    def __init__(
        self,
        ocr_repo: OCRRepository,
        doc_repo: DocumentRepository,
        member_repo: OrganizationMemberRepository,
    ) -> None:
        self.ocr_repo = ocr_repo
        self.doc_repo = doc_repo
        self.member_repo = member_repo

    async def _verify_org_membership(
        self, org_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """Validate user membership. Raises Forbidden if checks fail."""
        member = await self.member_repo.get_member(org_id, user_id)
        if not member:
            raise ForbiddenOrganizationActionException()

    async def create_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        data: OCRJobCreate,
    ) -> OCRJob:
        """Create new OCR job. Validates document exists and owns by org."""
        await self._verify_org_membership(org_id, user_id)

        # Verify document exists and belongs to the organization
        document = await self.doc_repo.get_by_id_and_org(data.document_id, org_id)
        if not document:
            raise DocumentNotFoundException()

        job = OCRJob(
            document_id=data.document_id,
            organization_id=org_id,
            owner_id=user_id,
            engine=data.engine,
            language=data.language,
            status="PENDING",
        )
        return await self.ocr_repo.create_job(job)

    async def get_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> OCRJob:
        """Retrieve details of specific OCR job. Validates org access."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ocr_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise OCRJobNotFoundException()
        return job

    async def list_jobs(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        status: str | None = None,
        engine: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[OCRJob]:
        """List OCR jobs in organization. Validates org access."""
        await self._verify_org_membership(org_id, user_id)
        return await self.ocr_repo.list_jobs_by_org(
            org_id, status=status, engine=engine, skip=skip, limit=limit
        )

    async def delete_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> None:
        """Permanently delete OCR job. Validates org access."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ocr_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise OCRJobNotFoundException()

        await self.ocr_repo.delete_job(job_id)

    async def cancel_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> OCRJob:
        """Cancel pending, queued, or running OCR job."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ocr_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise OCRJobNotFoundException()

        cancellable = {"PENDING", "QUEUED", "RUNNING"}
        if job.status not in cancellable:
            raise OCRJobNotCancellableException()

        update_dict = {
            "status": "CANCELLED",
            "updated_at": datetime.now(UTC),
        }
        updated = await self.ocr_repo.update_job(job_id, update_dict)
        if not updated:
            raise OCRJobNotFoundException()
        return updated

    async def retry_job(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> OCRJob:
        """Retry failed or cancelled OCR job."""
        await self._verify_org_membership(org_id, user_id)

        job = await self.ocr_repo.get_job_by_id_and_org(job_id, org_id)
        if not job:
            raise OCRJobNotFoundException()

        retriable = {"FAILED", "CANCELLED"}
        if job.status not in retriable:
            raise OCRJobNotRetriableException()

        # Delete any associated previous result before resetting
        await self.ocr_repo.delete_result_by_job_id(job_id)

        update_dict = {
            "status": "PENDING",
            "updated_at": datetime.now(UTC),
        }
        updated = await self.ocr_repo.update_job(job_id, update_dict)
        if not updated:
            raise OCRJobNotFoundException()
        return updated
