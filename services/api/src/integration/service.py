import uuid
from typing import Any, Sequence, cast
from services.api.src.integration.registry import ServiceRegistry
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


class IntegrationOrchestrator:
    """Orchestrator executing pipelines through interface bindings."""

    async def run_document_processing_pipeline(
        self,
        user_id: uuid.UUID,
        organization_id: uuid.UUID,
        document_id: uuid.UUID,
        file_size: int,
        recipient_email: str,
    ) -> dict[str, Any]:
        """Execute document processing pipeline across multiple module interfaces."""
        # 1. Resolve active services from registry
        storage = cast(IStorageService, ServiceRegistry.get(IStorageService))
        document = cast(IDocumentService, ServiceRegistry.get(IDocumentService))
        ocr = cast(IOCRService, ServiceRegistry.get(IOCRService))
        ai = cast(IAIService, ServiceRegistry.get(IAIService))
        audit = cast(IAuditService, ServiceRegistry.get(IAuditService))
        notification = cast(
            INotificationService, ServiceRegistry.get(INotificationService)
        )

        # 2. Storage Quota Check
        quota_ok = await storage.check_quota(organization_id, file_size)
        if not quota_ok:
            return {"status": "FAILED", "reason": "Storage Quota Exceeded"}

        # 3. Document Retrieval
        doc_metadata = await document.get_document(document_id)

        # 4. Trigger OCR Job
        ocr_result = await ocr.trigger_ocr(document_id, organization_id)
        ocr_job_id = ocr_result.get("job_id", uuid.uuid4())

        # 5. Run AI Analysis
        ai_result = await ai.run_analysis(
            document_id, ocr_job_id, organization_id
        )

        # 6. Write Audit Log Event
        await audit.log_event(
            user_id=user_id,
            organization_id=organization_id,
            event_type="Document",
            severity="Info",
            action="document.process_pipeline",
            resource_type="Document",
            resource_id=str(document_id),
        )

        # 7. Notify User
        doc_name = doc_metadata.get("original_filename", "document.pdf")
        await notification.dispatch_notification(
            user_id=user_id,
            notification_type="EMAIL",
            recipient=recipient_email,
            title="Ingestion pipeline finished",
            body=f"Your file '{doc_name}' was processed successfully.",
        )

        return {
            "status": "COMPLETED",
            "document_id": document_id,
            "ocr_job_id": ocr_job_id,
            "ai_result": ai_result,
        }


# ----------------------------------------------------
# Concrete Mock Service Implementations (Registry defaults)
# ----------------------------------------------------

class MockAuthService(IAuthService):
    async def authenticate_user(self, credentials: Any) -> Any:
        return {"authenticated": True, "user_id": uuid.uuid4()}


class MockUserService(IUserService):
    async def get_user_profile(self, user_id: uuid.UUID) -> Any:
        return {"user_id": user_id, "username": "mock_user", "is_active": True}


class MockOrganizationService(IOrganizationService):
    async def get_organization(self, organization_id: uuid.UUID) -> Any:
        return {"organization_id": organization_id, "name": "mock_org"}

    async def verify_member_role(
        self,
        user_id: uuid.UUID,
        organization_id: uuid.UUID,
        allowed_roles: Sequence[str],
    ) -> bool:
        return True


class MockDocumentService(IDocumentService):
    async def get_document(self, document_id: uuid.UUID) -> Any:
        return {
            "document_id": document_id,
            "original_filename": "invoice_receipt.pdf",
            "file_size": 102400,
        }


class MockOCRService(IOCRService):
    async def trigger_ocr(
        self, document_id: uuid.UUID, organization_id: uuid.UUID
    ) -> Any:
        return {
            "job_id": uuid.uuid4(),
            "document_id": document_id,
            "status": "SUCCESS",
            "engine": "paddleocr",
        }


class MockAIService(IAIService):
    async def run_analysis(
        self,
        document_id: uuid.UUID,
        ocr_result_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> Any:
        return {
            "analysis_id": uuid.uuid4(),
            "status": "SUCCESS",
            "extracted_fields": {"invoice_total": "120.00"},
        }


class MockWorkflowService(IWorkflowService):
    async def trigger_execution(
        self,
        workflow_id: uuid.UUID,
        document_id: uuid.UUID,
        organization_id: uuid.UUID,
        trigger_by: uuid.UUID,
    ) -> Any:
        return {"execution_id": uuid.uuid4(), "status": "COMPLETED"}


class MockSearchService(ISearchService):
    async def index_document(
        self, document_id: uuid.UUID, text_content: str
    ) -> Any:
        return {"indexed": True, "document_id": document_id}


class MockReportService(IReportService):
    async def queue_report_job(
        self, organization_id: uuid.UUID, report_type: str
    ) -> Any:
        return {"job_id": uuid.uuid4(), "status": "QUEUED"}


class MockNotificationService(INotificationService):
    async def dispatch_notification(
        self,
        user_id: uuid.UUID,
        notification_type: str,
        recipient: str,
        title: str | None,
        body: str,
    ) -> Any:
        return {"dispatched": True, "recipient": recipient}


class MockAuditService(IAuditService):
    async def log_event(
        self,
        user_id: uuid.UUID | None,
        organization_id: uuid.UUID | None,
        event_type: str,
        severity: str,
        action: str,
        resource_type: str | None,
        resource_id: str | None,
    ) -> Any:
        return {"logged": True, "action": action}


class MockStorageService(IStorageService):
    async def check_quota(self, organization_id: uuid.UUID, file_size: int) -> bool:
        return True


def register_mock_defaults() -> None:
    """Pre-populate the ServiceRegistry with default mock service bindings."""
    ServiceRegistry.register(IAuthService, MockAuthService())
    ServiceRegistry.register(IUserService, MockUserService())
    ServiceRegistry.register(IOrganizationService, MockOrganizationService())
    ServiceRegistry.register(IDocumentService, MockDocumentService())
    ServiceRegistry.register(IOCRService, MockOCRService())
    ServiceRegistry.register(IAIService, MockAIService())
    ServiceRegistry.register(IWorkflowService, MockWorkflowService())
    ServiceRegistry.register(ISearchService, MockSearchService())
    ServiceRegistry.register(IReportService, MockReportService())
    ServiceRegistry.register(INotificationService, MockNotificationService())
    ServiceRegistry.register(IAuditService, MockAuditService())
    ServiceRegistry.register(IStorageService, MockStorageService())
