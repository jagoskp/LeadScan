import React from 'react';
import { DeploymentChecklist } from '../types/release';

interface Props {
  checklist: DeploymentChecklist;
}

export const ProductionChecklistCard: React.FC<Props> = ({ checklist }) => {
  const items = [
    { label: 'Docker Container Readiness & Docker Compose Stack', ready: checklist.docker_ready },
    { label: 'CI/CD Pipeline Automated Test Verification', ready: checklist.ci_cd_ready },
    { label: 'Alembic Database Schema Migrations Applied', ready: checklist.database_migrations_applied },
    { label: 'Secret Vault Encryption Keys & OAuth Credentials', ready: checklist.vault_secrets_configured },
    { label: 'SSL/TLS In-Flight Data Encryption Enforced', ready: checklist.ssl_tls_enforced },
    { label: 'Multi-Tenant Organization Data Isolation Certified', ready: checklist.multi_tenant_isolation_certified },
  ];

  return (
    <div style={{ background: '#1a1d24', border: '1px solid #374151', borderRadius: '8px', padding: '20px', color: '#fff' }}>
      <h3 style={{ margin: '0 0 16px 0', fontSize: '1.1rem' }}>📋 DevOps Production Deployment Readiness Checklist</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {items.map((item, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#111827', padding: '12px 16px', borderRadius: '6px' }}>
            <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>{item.label}</span>
            <span style={{ color: item.ready ? '#10B981' : '#EF4444', fontWeight: 800, fontSize: '0.85rem' }}>
              {item.ready ? '✔ PASSED & CERTIFIED' : '✘ ACTION REQUIRED'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
