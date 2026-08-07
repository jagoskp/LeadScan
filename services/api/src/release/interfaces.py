from abc import ABC, abstractmethod
from typing import Any

from services.api.src.release.schemas import CertificationReportResponse, DeploymentChecklistResponse


class ICertificationEngine(ABC):

    @abstractmethod
    async def run_full_certification(self) -> CertificationReportResponse:
        pass


class ISecurityAuditor(ABC):

    @abstractmethod
    async def audit_security(self) -> dict[str, Any]:
        pass
