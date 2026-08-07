import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.src.database import get_db
from services.api.src.release.schemas import CertificationReportResponse, DeploymentChecklistResponse
from services.api.src.release.service import ReleaseCertificationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/release", tags=["Enterprise Release Candidate RC-1 Production Certification"])


@router.post("/certify", response_model=CertificationReportResponse, status_code=status.HTTP_201_CREATED)
async def run_full_certification(db: AsyncSession = Depends(get_db)):
    """Run full production certification audit across all GP-001 -> GP-020 and BF-001 -> BF-019 modules."""
    service = ReleaseCertificationService(db)
    return await service.run_certification()


@router.get("/security-audit")
async def get_security_audit(db: AsyncSession = Depends(get_db)):
    """Get security certification audit report."""
    service = ReleaseCertificationService(db)
    return await service.get_security_audit()


@router.get("/performance-audit")
async def get_performance_audit(db: AsyncSession = Depends(get_db)):
    """Get performance throughput and search latency benchmarks."""
    service = ReleaseCertificationService(db)
    return await service.get_performance_audit()


@router.get("/backup-audit")
async def get_backup_audit(db: AsyncSession = Depends(get_db)):
    """Get backup and disaster recovery verification audit."""
    service = ReleaseCertificationService(db)
    return await service.get_backup_recovery_audit()


@router.get("/deployment-checklist", response_model=DeploymentChecklistResponse)
async def get_deployment_checklist(db: AsyncSession = Depends(get_db)):
    """Get DevOps production deployment readiness checklist."""
    service = ReleaseCertificationService(db)
    return await service.get_deployment_checklist()
