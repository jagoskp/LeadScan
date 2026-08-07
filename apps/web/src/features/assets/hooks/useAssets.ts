import { useCallback, useEffect, useState } from 'react';
import { assetsApi } from '../services/assetsApi';
import { Asset } from '../types/assets';

export function useAssets(initialType?: string) {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [assetType, setAssetType] = useState<string | undefined>(initialType);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchAssets = useCallback(async () => {
    setLoading(true);
    try {
      const list = await assetsApi.listAssets(assetType);
      setAssets(list);
    } catch (e) {
      console.error('Failed to load assets', e);
    } finally {
      setLoading(false);
    }
  }, [assetType]);

  useEffect(() => {
    fetchAssets();
  }, [fetchAssets]);

  return { assets, assetType, setAssetType, loading, refetchAssets: fetchAssets };
}
