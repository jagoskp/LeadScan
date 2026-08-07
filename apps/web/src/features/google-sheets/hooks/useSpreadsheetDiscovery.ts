import { useCallback, useEffect, useState } from 'react';
import { googleSheetsApi } from '../services/googleSheetsApi';
import { Spreadsheet, Worksheet } from '../types/googleSheets';

export function useSpreadsheetDiscovery(accountId: string | null) {
  const [spreadsheets, setSpreadsheets] = useState<Spreadsheet[]>([]);
  const [worksheets, setWorksheets] = useState<Worksheet[]>([]);
  const [selectedSpreadsheetId, setSelectedSpreadsheetId] = useState<string | null>(null);
  const [selectedWorksheetTitle, setSelectedWorksheetTitle] = useState<string | null>(null);
  const [loadingSpreadsheets, setLoadingSpreadsheets] = useState<boolean>(false);
  const [loadingWorksheets, setLoadingWorksheets] = useState<boolean>(false);

  const fetchSpreadsheets = useCallback(async () => {
    if (!accountId) return;
    setLoadingSpreadsheets(true);
    try {
      const list = await googleSheetsApi.getSpreadsheets(accountId);
      setSpreadsheets(list);
      if (list.length > 0) {
        setSelectedSpreadsheetId(list[0].id);
      }
    } catch (e) {
      console.error('Failed to discover spreadsheets', e);
    } finally {
      setLoadingSpreadsheets(false);
    }
  }, [accountId]);

  const fetchWorksheets = useCallback(async () => {
    if (!accountId || !selectedSpreadsheetId) return;
    setLoadingWorksheets(true);
    try {
      const list = await googleSheetsApi.getWorksheets(accountId, selectedSpreadsheetId);
      setWorksheets(list);
      if (list.length > 0) {
        setSelectedWorksheetTitle(list[0].title);
      }
    } catch (e) {
      console.error('Failed to discover worksheets', e);
    } finally {
      setLoadingWorksheets(false);
    }
  }, [accountId, selectedSpreadsheetId]);

  useEffect(() => {
    fetchSpreadsheets();
  }, [fetchSpreadsheets]);

  useEffect(() => {
    fetchWorksheets();
  }, [fetchWorksheets]);

  return {
    spreadsheets,
    worksheets,
    selectedSpreadsheetId,
    setSelectedSpreadsheetId,
    selectedWorksheetTitle,
    setSelectedWorksheetTitle,
    loadingSpreadsheets,
    loadingWorksheets,
  };
}
