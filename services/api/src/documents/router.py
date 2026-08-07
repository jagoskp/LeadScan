import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.documents.dependencies import get_document_service
from services.api.src.documents.schemas import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from services.api.src.documents.service import DocumentService

router = APIRouter(prefix="/organizations/{org_id}/documents", tags=["documents"])


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document_metadata(
    org_id: uuid.UUID,
    data: DocumentCreate,
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> Any:
    """Upload metadata for a new document under an organization."""
    return await doc_service.create_document(
        org_id=org_id,
        user_id=current_user.id,
        data=data,
    )


@router.get("/search", response_model=list[DocumentResponse])
async def search_documents(
    org_id: uuid.UUID,
    q: str = Query(
        ..., min_length=1, description="Substring search query for filenames"
    ),  # noqa: B008
    skip: int = Query(0, ge=0),  # noqa: B008
    limit: int = Query(100, ge=1, le=100),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> Any:
    """Search documents by filename under an organization."""
    return await doc_service.search_documents(
        org_id=org_id,
        user_id=current_user.id,
        query=q,
        skip=skip,
        limit=limit,
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    org_id: uuid.UUID,
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> Any:
    """Retrieve details for a specific document metadata record."""
    return await doc_service.get_document(
        org_id=org_id,
        user_id=current_user.id,
        doc_id=document_id,
    )


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    org_id: uuid.UUID,
    status: str | None = Query(
        None, description="Filter by status (e.g., ACTIVE, ARCHIVED)"
    ),  # noqa: B008
    skip: int = Query(0, ge=0),  # noqa: B008
    limit: int = Query(100, ge=1, le=100),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> Any:
    """List documents registered under the organization workspace."""
    return await doc_service.list_documents(
        org_id=org_id,
        user_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document_metadata(
    org_id: uuid.UUID,
    document_id: uuid.UUID,
    data: DocumentUpdate,
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> Any:
    """Update metadata for an existing document."""
    return await doc_service.update_document_metadata(
        org_id=org_id,
        user_id=current_user.id,
        doc_id=document_id,
        data=data,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    org_id: uuid.UUID,
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> None:
    """Permanently delete a document metadata record."""
    await doc_service.delete_document(
        org_id=org_id,
        user_id=current_user.id,
        doc_id=document_id,
    )


@router.post("/{document_id}/archive", response_model=DocumentResponse)
async def archive_document(
    org_id: uuid.UUID,
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> Any:
    """Archive a document by transitioning its status to ARCHIVED."""
    return await doc_service.archive_document(
        org_id=org_id,
        user_id=current_user.id,
        doc_id=document_id,
    )


@router.post("/{document_id}/restore", response_model=DocumentResponse)
async def restore_document(
    org_id: uuid.UUID,
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),  # noqa: B008
    doc_service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> Any:
    """Restore an archived document back to ACTIVE status."""
    return await doc_service.restore_document(
        org_id=org_id,
        user_id=current_user.id,
        doc_id=document_id,
    )
