import { useCallback, useEffect, useState } from 'react';
import { leadsApi } from '../services/leadsApi';
import { Lead } from '../types/leads';

export function useLeads(initialSearch?: string, initialStatus?: string, isArchived: boolean = false) {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [search, setSearch] = useState<string>(initialSearch || '');
  const [status, setStatus] = useState<string>(initialStatus || '');
  const [loading, setLoading] = useState<boolean>(false);

  const fetchLeads = useCallback(async () => {
    setLoading(true);
    try {
      const list = await leadsApi.listLeads(search, status, isArchived);
      setLeads(list);
    } catch (e) {
      console.error('Failed to load leads', e);
    } finally {
      setLoading(false);
    }
  }, [search, status, isArchived]);

  useEffect(() => {
    fetchLeads();
  }, [fetchLeads]);

  return {
    leads,
    search,
    setSearch,
    status,
    setStatus,
    loading,
    refetchLeads: fetchLeads,
  };
}
