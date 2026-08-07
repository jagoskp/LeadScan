import { useCallback, useEffect, useState } from 'react';
import { googleSheetsApi } from '../services/googleSheetsApi';
import { MappingValidationReport, SyncHistoryItem, SyncJob } from '../types/googleSheets';

export function useGoogleSync(
  accountId: string | null,
  spreadsheetId: string | null,
  worksheetTitle: string | null
) {
  const [history, setHistory] = useState<SyncHistoryItem[]>([]);
  const [validationReport, setValidationReport] = useState<MappingValidationReport | null>(null);
  const [syncing, setSyncing] = useState<boolean>(false);
  const [loadingHistory, setLoadingHistory] = useState<boolean>(false);

  const fetchHistory = useCallback(async () => {
    setLoadingHistory(true);
    try {
      const list = await googleSheetsApi.getHistory();
      setHistory(list);
    } catch (e) {
      console.error('Failed to load history', e);
    } finally {
      setLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const runPreSyncCheck = async (profileId: string) => {
    if (!accountId || !spreadsheetId || !worksheetTitle) return null;
    try {
      const report = await googleSheetsApi.preSyncCheck(accountId, profileId, spreadsheetId, worksheetTitle);
      setValidationReport(report);
      return report;
    } catch (e) {
      console.error('Pre-sync check failed', e);
      return null;
    }
  };

  const executeSync = async (
    profileId: string,
    syncMode: string,
    rowsData: Record<string, unknown>[],
    autoApplyRemapping: boolean = true
  ): Promise<SyncJob | null> => {
    if (!accountId || !spreadsheetId || !worksheetTitle) return null;
    setSyncing(true);
    try {
      const job = await googleSheetsApi.executeSync(accountId, {
        profile_id: profileId,
        spreadsheet_id: spreadsheetId,
        worksheet_title: worksheetTitle,
        sync_mode: syncMode,
        rows_data: rowsData,
        auto_apply_remapping: autoApplyRemapping,
      });
      await fetchHistory();
      return job;
    } catch (e) {
      console.error('Sync failed', e);
      throw e;
    } finally {
      setSyncing(false);
    }
  };

  return {
    history,
    validationReport,
    syncing,
    loadingHistory,
    runPreSyncCheck,
    executeSync,
    refetchHistory: fetchHistory,
  };
}
