import { useCallback, useEffect, useState } from 'react';
import { assetsApi } from '../services/assetsApi';
import { Asset } from '../types/assets';

export function useAssetDetail(assetId: string | null) {
  const [asset, setAsset] = useState<Asset | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchAsset = useCallback(async () => {
    if (!assetId) return;
    setLoading(true);
    try {
      const data = await assetsApi.getAsset(assetId);
      setAsset(data);
    } catch (e) {
      console.error('Failed to load asset details', e);
    } finally {
      setLoading(false);
    }
  }, [assetId]);

  useEffect(() => {
    fetchAsset();
  }, [fetchAsset]);

  return { asset, loading, refetchAsset: fetchAsset };
}
