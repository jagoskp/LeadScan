from typing import cast
from services.api.src.integration.registry import ServiceRegistry
from services.api.src.integration.service import IntegrationOrchestrator
from services.api.src.integration.interfaces import (
    IAuthService,
    IUserService,
    IOrganizationService,
    IDocumentService,
    IOCRService,
    IAIService,
    IWorkflowService,
    ISearchService,
    IReportService,
    INotificationService,
    IAuditService,
    IStorageService,
)


def get_integration_orchestrator() -> IntegrationOrchestrator:
    """Inject IntegrationOrchestrator service instance."""
    return IntegrationOrchestrator()


def get_auth_service() -> IAuthService:
    """Inject current registered IAuthService implementation."""
    return cast(IAuthService, ServiceRegistry.get(IAuthService))


def get_user_service() -> IUserService:
    """Inject current registered IUserService implementation."""
    return cast(IUserService, ServiceRegistry.get(IUserService))


def get_organization_service() -> IOrganizationService:
    """Inject current registered IOrganizationService implementation."""
    return cast(IOrganizationService, ServiceRegistry.get(IOrganizationService))


def get_document_service() -> IDocumentService:
    """Inject current registered IDocumentService implementation."""
    return cast(IDocumentService, ServiceRegistry.get(IDocumentService))


def get_ocr_service() -> IOCRService:
    """Inject current registered IOCRService implementation."""
    return cast(IOCRService, ServiceRegistry.get(IOCRService))


def get_ai_service() -> IAIService:
    """Inject current registered IAIService implementation."""
    return cast(IAIService, ServiceRegistry.get(IAIService))


def get_workflow_service() -> IWorkflowService:
    """Inject current registered IWorkflowService implementation."""
    return cast(IWorkflowService, ServiceRegistry.get(IWorkflowService))


def get_search_service() -> ISearchService:
    """Inject current registered ISearchService implementation."""
    return cast(ISearchService, ServiceRegistry.get(ISearchService))


def get_report_service() -> IReportService:
    """Inject current registered IReportService implementation."""
    return cast(IReportService, ServiceRegistry.get(IReportService))


def get_notification_service() -> INotificationService:
    """Inject current registered INotificationService implementation."""
    return cast(INotificationService, ServiceRegistry.get(INotificationService))


def get_audit_service() -> IAuditService:
    """Inject current registered IAuditService implementation."""
    return cast(IAuditService, ServiceRegistry.get(IAuditService))


def get_storage_service() -> IStorageService:
    """Inject current registered IStorageService implementation."""
    return cast(IStorageService, ServiceRegistry.get(IStorageService))
