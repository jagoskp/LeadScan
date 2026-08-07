import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.release.backup_recovery import BackupRecoveryVerifier
from services.api.src.release.certification import CertificationEngine
from services.api.src.release.performance import PerformanceAuditor
from services.api.src.release.repository import ReleaseRepository
from services.api.src.release.schemas import CertificationReportResponse, DeploymentChecklistResponse
from services.api.src.release.security_audit import SecurityAuditor

logger = logging.getLogger(__name__)


class ReleaseCertificationService:
    """Facade Application Service for Enterprise Release Candidate (RC-1) Production Certification."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ReleaseRepository(db)
        self.cert_engine = CertificationEngine(db)
        self.security_auditor = SecurityAuditor(db)
        self.performance_auditor = PerformanceAuditor(db)
        self.backup_verifier = BackupRecoveryVerifier(db)

    async def run_certification(self) -> CertificationReportResponse:
        return await self.cert_engine.run_full_certification()

    async def get_security_audit(self) -> dict[str, Any]:
        return await self.security_auditor.audit_security()

    async def get_performance_audit(self) -> dict[str, Any]:
        return await self.performance_auditor.audit_performance()

    async def get_backup_recovery_audit(self) -> dict[str, Any]:
        return await self.backup_verifier.verify_backup_recovery()

    async def get_deployment_checklist(self) -> DeploymentChecklistResponse:
        return DeploymentChecklistResponse()
