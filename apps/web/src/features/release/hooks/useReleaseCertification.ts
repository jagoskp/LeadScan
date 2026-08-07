import { useCallback, useEffect, useState } from 'react';
import { releaseApi } from '../services/releaseApi';
import { CertificationReport, DeploymentChecklist } from '../types/release';

export function useReleaseCertification() {
  const [report, setReport] = useState<CertificationReport | null>(null);
  const [checklist, setChecklist] = useState<DeploymentChecklist | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const runCertification = useCallback(async () => {
    setLoading(true);
    try {
      const rep = await releaseApi.runFullCertification();
      const chk = await releaseApi.getDeploymentChecklist();
      setReport(rep);
      setChecklist(chk);
    } catch (e) {
      console.error('Failed to run production certification', e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    runCertification();
  }, [runCertification]);

  return { report, checklist, loading, refetch: runCertification };
}
