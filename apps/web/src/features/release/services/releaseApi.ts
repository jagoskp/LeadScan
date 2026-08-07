import { CertificationReport, DeploymentChecklist } from '../types/release';

const BASE_URL = '/api/v1/release';

export const releaseApi = {
  async runFullCertification(): Promise<CertificationReport> {
    const res = await fetch(`${BASE_URL}/certify`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to execute full production certification audit');
    return res.json();
  },

  async getDeploymentChecklist(): Promise<DeploymentChecklist> {
    const res = await fetch(`${BASE_URL}/deployment-checklist`);
    if (!res.ok) throw new Error('Failed to fetch deployment checklist');
    return res.json();
  },

  async getSecurityAudit(): Promise<Record<string, unknown>> {
    const res = await fetch(`${BASE_URL}/security-audit`);
    if (!res.ok) throw new Error('Failed to fetch security audit');
    return res.json();
  },
};
