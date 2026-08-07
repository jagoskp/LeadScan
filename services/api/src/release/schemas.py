import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class CertificationCheckItem(BaseModel):
    category: str
    component: str
    status: str = "PASS"
    details: str


class CertificationReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    release_version: str
    certification_status: str
    audited_by: str
    overall_score: float
    checks: list[CertificationCheckItem]
    created_at: datetime


class DeploymentChecklistResponse(BaseModel):
    docker_ready: bool = True
    ci_cd_ready: bool = True
    database_migrations_applied: bool = True
    vault_secrets_configured: bool = True
    ssl_tls_enforced: bool = True
    multi_tenant_isolation_certified: bool = True
