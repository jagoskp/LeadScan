# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.document_model.dependencies import (
    get_dom_engine_service,
)
from services.api.src.document_model.schemas import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
    EntityAttributeResponse,
    EntityAttributeUpdate,
    EntityResponse,
)
from services.api.src.document_model.service import DOMEngineService

router = APIRouter(prefix="/dom", tags=["document_model"])


# ----------------------------------------------------
# DOM Documents Endpoints
# ----------------------------------------------------

@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dom_document(
    data: DocumentCreate,
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> Any:
    """Create a new DOM Document root config."""
    return await service.create_document(user_id=current_user.id, data=data)


@router.get("/documents", response_model=list[DocumentResponse])
async def list_dom_documents(
    organization_id: uuid.UUID | None = Query(
        None, description="Filter by organization"
    ),
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> Any:
    """List DOM Documents filtered by user context and organization."""
    return await service.list_documents(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_dom_document(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> Any:
    """Retrieve detailed properties of a single DOM Document."""
    return await service.get_document(document_id)


@router.patch("/documents/{document_id}", response_model=DocumentResponse)
async def update_dom_document(
    document_id: uuid.UUID,
    data: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> Any:
    """Update DOM Document review status."""
    return await service.update_document_status(document_id, data)


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dom_document(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> None:
    """Delete a DOM Document root."""
    await service.delete_document(document_id)


@router.post(
    "/documents/build",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def build_document_dom(
    understanding_job_id: uuid.UUID = Query(
        ..., description="Source AI Job ID reference"
    ),
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> Any:
    """Parse AI understanding job and build structural DOM tree nodes."""
    doc_id = await service.build_dom(understanding_job_id)
    return await service.get_document(doc_id)


# ----------------------------------------------------
# DOM Entities & Attributes Endpoints
# ----------------------------------------------------

@router.get("/entities/{entity_id}", response_model=EntityResponse)
async def get_dom_entity(
    entity_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> Any:
    """Retrieve detailed properties of a single DOM Entity."""
    return await service.get_entity(entity_id)


@router.patch("/attributes/{attr_id}", response_model=EntityAttributeResponse)
async def update_dom_attribute(
    attr_id: uuid.UUID,
    data: EntityAttributeUpdate,
    current_user: User = Depends(get_current_user),
    service: DOMEngineService = Depends(get_dom_engine_service),
) -> Any:
    """Update review status or values of a target DOM Entity Attribute."""
    return await service.update_attribute(attr_id, data)
