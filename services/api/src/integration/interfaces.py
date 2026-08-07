import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IAuthService(ABC):
    """Interface for Authentication services."""

    @abstractmethod
    async def authenticate_user(self, credentials: Any) -> Any:
        pass


class IUserService(ABC):
    """Interface for User management services."""

    @abstractmethod
    async def get_user_profile(self, user_id: uuid.UUID) -> Any:
        pass


class IOrganizationService(ABC):
    """Interface for Organization tenant services."""

    @abstractmethod
    async def get_organization(self, organization_id: uuid.UUID) -> Any:
        pass

    @abstractmethod
    async def verify_member_role(
        self,
        user_id: uuid.UUID,
        organization_id: uuid.UUID,
        allowed_roles: Sequence[str],
    ) -> bool:
        pass


class IDocumentService(ABC):
    """Interface for Document ingestion services."""

    @abstractmethod
    async def get_document(self, document_id: uuid.UUID) -> Any:
        pass


class IOCRService(ABC):
    """Interface for OCR processing services."""

    @abstractmethod
    async def trigger_ocr(
        self, document_id: uuid.UUID, organization_id: uuid.UUID
    ) -> Any:
        pass


class IAIService(ABC):
    """Interface for AI analysis services."""

    @abstractmethod
    async def run_analysis(
        self,
        document_id: uuid.UUID,
        ocr_result_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> Any:
        pass


class IWorkflowService(ABC):
    """Interface for Workflow orchestration services."""

    @abstractmethod
    async def trigger_execution(
        self,
        workflow_id: uuid.UUID,
        document_id: uuid.UUID,
        organization_id: uuid.UUID,
        trigger_by: uuid.UUID,
    ) -> Any:
        pass


class ISearchService(ABC):
    """Interface for indexing and Search query services."""

    @abstractmethod
    async def index_document(self, document_id: uuid.UUID, text_content: str) -> Any:
        pass


class IReportService(ABC):
    """Interface for analytics Reports services."""

    @abstractmethod
    async def queue_report_job(
        self, organization_id: uuid.UUID, report_type: str
    ) -> Any:
        pass


class INotificationService(ABC):
    """Interface for Notifications delivery services."""

    @abstractmethod
    async def dispatch_notification(
        self,
        user_id: uuid.UUID,
        notification_type: str,
        recipient: str,
        title: str | None,
        body: str,
    ) -> Any:
        pass


class IAuditService(ABC):
    """Interface for Audit Log logging services."""

    @abstractmethod
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
        pass


class IStorageService(ABC):
    """Interface for Storage quota and files services."""

    @abstractmethod
    async def check_quota(self, organization_id: uuid.UUID, file_size: int) -> bool:
        pass
