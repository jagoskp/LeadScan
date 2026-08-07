import { useCallback, useEffect, useState } from 'react';
import { leadsApi } from '../services/leadsApi';
import { Lead } from '../types/leads';

export function useLeadDetail(leadId: string | null) {
  const [lead, setLead] = useState<Lead | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchLead = useCallback(async () => {
    if (!leadId) return;
    setLoading(true);
    try {
      const data = await leadsApi.getLead(leadId);
      setLead(data);
    } catch (e) {
      console.error('Failed to load lead detail', e);
    } finally {
      setLoading(false);
    }
  }, [leadId]);

  useEffect(() => {
    fetchLead();
  }, [fetchLead]);

  return { lead, loading, refetchLead: fetchLead };
}
