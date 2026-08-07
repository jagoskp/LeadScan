import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import UTC, datetime

from services.api.src.release.backup_recovery import BackupRecoveryVerifier
from services.api.src.release.certification import CertificationEngine
from services.api.src.release.performance import PerformanceAuditor
from services.api.src.release.security_audit import SecurityAuditor
from services.api.src.release.service import ReleaseCertificationService


@pytest.fixture
def mock_db():
    db = AsyncMock()
    now = datetime.now(UTC)

    async def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        res.scalars.return_value.first.return_value = None
        return res

    db.execute.side_effect = mock_execute
    return db


@pytest.mark.asyncio
async def test_full_system_certification_audit(mock_db):
    service = ReleaseCertificationService(mock_db)
    report = await service.run_certification()

    assert report.release_version == "1.0.0-RC1"
    assert report.certification_status == "CERTIFIED"
    assert report.overall_score == 100.0
    assert len(report.checks) >= 10


@pytest.mark.asyncio
async def test_security_audit_and_performance_benchmarks(mock_db):
    service = ReleaseCertificationService(mock_db)

    sec_report = await service.get_security_audit()
    assert sec_report["rbac_enforcement"] == "VERIFIED_PASS"
    assert sec_report["security_rating"] == "A+"

    perf_report = await service.get_performance_audit()
    assert perf_report["performance_status"] == "ENTERPRISE_READY"

    backup_report = await service.get_backup_recovery_audit()
    assert backup_report["backup_verification_status"] == "CERTIFIED"

    checklist = await service.get_deployment_checklist()
    assert checklist.docker_ready is True
    assert checklist.multi_tenant_isolation_certified is True
