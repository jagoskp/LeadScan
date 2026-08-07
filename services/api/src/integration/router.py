# ruff: noqa: B008
import uuid
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from services.api.src.auth.dependencies import get_current_user
from services.api.src.auth.models import User
from services.api.src.integration.dependencies import get_integration_orchestrator
from services.api.src.integration.registry import ServiceRegistry
from services.api.src.integration.service import IntegrationOrchestrator

router = APIRouter(prefix="/integration", tags=["integration"])


class OrchestrationRequest(BaseModel):
    organization_id: uuid.UUID
    document_id: uuid.UUID
    file_size: int = Field(1024, ge=0)
    recipient_email: str = Field("user@example.com", min_length=3)


# ----------------------------------------------------
# Integration Layer Health & Registry Endpoints
# ----------------------------------------------------


@router.get("/health", status_code=status.HTTP_200_OK)
async def get_integration_health(
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Retrieve health and availability status of the Integration Layer framework."""
    bindings = ServiceRegistry.get_bindings()
    expected_interfaces = [
        "IAuthService",
        "IUserService",
        "IOrganizationService",
        "IDocumentService",
        "IOCRService",
        "IAIService",
        "IWorkflowService",
        "ISearchService",
        "IReportService",
        "INotificationService",
        "IAuditService",
        "IStorageService",
    ]

    missing_interfaces = [i for i in expected_interfaces if i not in bindings]
    is_healthy = len(missing_interfaces) == 0

    return {
        "status": "HEALTHY" if is_healthy else "DEGRADED",
        "framework": "LeadScan AI Integration Foundation",
        "active_bindings_count": len(bindings),
        "missing_bindings": missing_interfaces,
    }


@router.get("/registry", status_code=status.HTTP_200_OK)
async def get_service_registry(
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """List active abstract interface bindings in the ServiceRegistry."""
    return {
        "registry": "ServiceRegistry",
        "bindings": ServiceRegistry.get_bindings(),
    }


@router.post("/orchestrate", status_code=status.HTTP_200_OK)
async def trigger_orchestration_pipeline(
    data: OrchestrationRequest,
    current_user: User = Depends(get_current_user),
    service: IntegrationOrchestrator = Depends(get_integration_orchestrator),
) -> Any:
    """Trigger the coordinate cross-module mock document ingestion workflow."""
    return await service.run_document_processing_pipeline(
        user_id=current_user.id,
        organization_id=data.organization_id,
        document_id=data.document_id,
        file_size=data.file_size,
        recipient_email=data.recipient_email,
    )
