export interface CertificationCheckItem {
  category: string;
  component: string;
  status: 'PASS' | 'FAIL' | 'WARNING';
  details: string;
}

export interface CertificationReport {
  id: string;
  release_version: string;
  certification_status: string;
  audited_by: string;
  overall_score: number;
  checks: CertificationCheckItem[];
  created_at: string;
}

export interface DeploymentChecklist {
  docker_ready: boolean;
  ci_cd_ready: boolean;
  database_migrations_applied: boolean;
  vault_secrets_configured: boolean;
  ssl_tls_enforced: boolean;
  multi_tenant_isolation_certified: boolean;
}
