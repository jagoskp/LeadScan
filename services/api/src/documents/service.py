import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from services.api.src.documents.exceptions import (
    DocumentAlreadyArchivedException,
    DocumentNotArchivedException,
    DocumentNotFoundException,
)
from services.api.src.documents.models import Document
from services.api.src.documents.repository import DocumentRepository
from services.api.src.documents.schemas import DocumentCreate, DocumentUpdate
from services.api.src.organization.exceptions import (
    ForbiddenOrganizationActionException,
)
from services.api.src.organization.repository import OrganizationMemberRepository


class DocumentService:
    """Service coordinates Document lifecycle and organization checks."""

    def __init__(
        self,
        doc_repo: DocumentRepository,
        member_repo: OrganizationMemberRepository,
    ) -> None:
        self.doc_repo = doc_repo
        self.member_repo = member_repo

    async def _verify_org_membership(
        self, org_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """Validate user membership inside organization. Raises Forbidden if fails."""
        member = await self.member_repo.get_member(org_id, user_id)
        if not member:
            raise ForbiddenOrganizationActionException()

    async def create_document(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        data: DocumentCreate,
    ) -> Document:
        """Persist new document metadata. Validates organization access."""
        await self._verify_org_membership(org_id, user_id)

        document = Document(
            organization_id=org_id,
            owner_id=user_id,
            filename=data.filename,
            original_filename=data.original_filename,
            file_type=data.file_type,
            mime_type=data.mime_type,
            file_size=data.file_size,
            storage_path=data.storage_path,
            status="ACTIVE",
        )
        return await self.doc_repo.create(document)

    async def get_document(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        doc_id: uuid.UUID,
    ) -> Document:
        """Retrieve document metadata. Validates organization access."""
        await self._verify_org_membership(org_id, user_id)

        document = await self.doc_repo.get_by_id_and_org(doc_id, org_id)
        if not document:
            raise DocumentNotFoundException()
        return document

    async def list_documents(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Document]:
        """List documents under an organization workspace."""
        await self._verify_org_membership(org_id, user_id)
        return await self.doc_repo.list_by_org(
            org_id, status=status, skip=skip, limit=limit
        )

    async def update_document_metadata(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        doc_id: uuid.UUID,
        data: DocumentUpdate,
    ) -> Document:
        """Modify document metadata fields. Validates organization access."""
        await self._verify_org_membership(org_id, user_id)

        document = await self.doc_repo.get_by_id_and_org(doc_id, org_id)
        if not document:
            raise DocumentNotFoundException()

        update_dict: dict[str, Any] = {}
        if data.filename is not None:
            update_dict["filename"] = data.filename
        if data.file_type is not None:
            update_dict["file_type"] = data.file_type
        if data.mime_type is not None:
            update_dict["mime_type"] = data.mime_type

        if update_dict:
            update_dict["updated_at"] = datetime.now(UTC)
            updated = await self.doc_repo.update(doc_id, update_dict)
            if not updated:
                raise DocumentNotFoundException()
            return updated

        return document

    async def delete_document(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        doc_id: uuid.UUID,
    ) -> None:
        """Permanently delete document metadata. Validates organization access."""
        await self._verify_org_membership(org_id, user_id)

        document = await self.doc_repo.get_by_id_and_org(doc_id, org_id)
        if not document:
            raise DocumentNotFoundException()

        await self.doc_repo.delete(doc_id)

    async def archive_document(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        doc_id: uuid.UUID,
    ) -> Document:
        """Transition document status to ARCHIVED. Validates organization access."""
        await self._verify_org_membership(org_id, user_id)

        document = await self.doc_repo.get_by_id_and_org(doc_id, org_id)
        if not document:
            raise DocumentNotFoundException()

        if document.status == "ARCHIVED":
            raise DocumentAlreadyArchivedException()

        update_dict = {
            "status": "ARCHIVED",
            "updated_at": datetime.now(UTC),
        }
        updated = await self.doc_repo.update(doc_id, update_dict)
        if not updated:
            raise DocumentNotFoundException()
        return updated

    async def restore_document(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        doc_id: uuid.UUID,
    ) -> Document:
        """Restore archived document. Validates organization access."""
        await self._verify_org_membership(org_id, user_id)

        document = await self.doc_repo.get_by_id_and_org(doc_id, org_id)
        if not document:
            raise DocumentNotFoundException()

        if document.status != "ARCHIVED":
            raise DocumentNotArchivedException()

        update_dict = {
            "status": "ACTIVE",
            "updated_at": datetime.now(UTC),
        }
        updated = await self.doc_repo.update(doc_id, update_dict)
        if not updated:
            raise DocumentNotFoundException()
        return updated

    async def search_documents(
        self,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        query: str,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Document]:
        """Search documents by matching pattern in name/original name."""
        await self._verify_org_membership(org_id, user_id)
        return await self.doc_repo.search_by_org(
            org_id, query=query, skip=skip, limit=limit
        )
