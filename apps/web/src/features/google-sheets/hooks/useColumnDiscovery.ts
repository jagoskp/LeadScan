import { useCallback, useEffect, useState } from 'react';
import { googleSheetsApi } from '../services/googleSheetsApi';
import { ColumnDiscoveryResponse } from '../types/googleSheets';

export function useColumnDiscovery(
  accountId: string | null,
  spreadsheetId: string | null,
  worksheetTitle: string | null
) {
  const [discovery, setDiscovery] = useState<ColumnDiscoveryResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchColumns = useCallback(async () => {
    if (!accountId || !spreadsheetId || !worksheetTitle) return;
    setLoading(true);
    try {
      const res = await googleSheetsApi.getColumns(accountId, spreadsheetId, worksheetTitle);
      setDiscovery(res);
    } catch (e) {
      console.error('Failed to discover columns', e);
    } finally {
      setLoading(false);
    }
  }, [accountId, spreadsheetId, worksheetTitle]);

  useEffect(() => {
    fetchColumns();
  }, [fetchColumns]);

  return { discovery, loading, refetchColumns: fetchColumns };
}
