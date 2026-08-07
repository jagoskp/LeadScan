import { useCallback, useEffect, useState } from 'react';
import { identityApi } from '../services/identityApi';
import { MergePreviewResponse } from '../types/identity';

export function useMergePreview(primaryId: string | null, secondaryId: string | null) {
  const [preview, setPreview] = useState<MergePreviewResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchPreview = useCallback(async () => {
    if (!primaryId || !secondaryId) return;
    setLoading(true);
    try {
      const data = await identityApi.getMergePreview(primaryId, secondaryId);
      setPreview(data);
    } catch (e) {
      console.error('Failed to load merge preview', e);
    } finally {
      setLoading(false);
    }
  }, [primaryId, secondaryId]);

  useEffect(() => {
    fetchPreview();
  }, [fetchPreview]);

  return { preview, loading, refetchPreview: fetchPreview };
}
