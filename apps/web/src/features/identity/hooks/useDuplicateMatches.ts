import { useCallback, useEffect, useState } from 'react';
import { identityApi } from '../services/identityApi';
import { DuplicateMatch } from '../types/identity';

export function useDuplicateMatches(initialStatus: string = 'pending') {
  const [matches, setMatches] = useState<DuplicateMatch[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchMatches = useCallback(async () => {
    setLoading(true);
    try {
      const list = await identityApi.listDuplicateMatches(initialStatus);
      setMatches(list);
    } catch (e) {
      console.error('Failed to load duplicate matches', e);
    } finally {
      setLoading(false);
    }
  }, [initialStatus]);

  useEffect(() => {
    fetchMatches();
  }, [fetchMatches]);

  const triggerScan = async () => {
    setLoading(true);
    try {
      const list = await identityApi.scanForDuplicates();
      setMatches(list);
    } catch (e) {
      console.error('Duplicate scan error', e);
    } finally {
      setLoading(false);
    }
  };

  return { matches, loading, triggerScan, refetchMatches: fetchMatches };
}
