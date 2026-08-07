import { useCallback, useEffect, useState } from 'react';
import { assetsApi } from '../services/assetsApi';
import { CompanyLogo } from '../types/assets';

export function useCompanyLogo(companyId: string | null) {
  const [logo, setLogo] = useState<CompanyLogo | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchLogo = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const data = await assetsApi.getCompanyLogo(companyId);
      setLogo(data);
    } catch (e) {
      console.error('Failed to load company logo', e);
    } finally {
      setLoading(false);
    }
  }, [companyId]);

  useEffect(() => {
    fetchLogo();
  }, [fetchLogo]);

  return { logo, loading, refetchLogo: fetchLogo };
}
