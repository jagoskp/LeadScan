import { useCallback, useEffect, useState } from 'react';
import { googleSheetsApi } from '../services/googleSheetsApi';
import { GoogleAccount } from '../types/googleSheets';

export function useGoogleOAuth() {
  const [accounts, setAccounts] = useState<GoogleAccount[]>([]);
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchAccounts = useCallback(async () => {
    setLoading(true);
    try {
      const list = await googleSheetsApi.getAccounts();
      setAccounts(list);
      if (list.length > 0 && !selectedAccountId) {
        setSelectedAccountId(list[0].id);
      }
    } catch (e) {
      console.error('Failed to load Google Accounts', e);
    } finally {
      setLoading(false);
    }
  }, [selectedAccountId]);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  const handleConnect = async () => {
    try {
      const { authorization_url } = await googleSheetsApi.getAuthUrl();
      // Execute OAuth code exchange mock / window redirect
      const mockCode = `mock_code_${Date.now()}`;
      await googleSheetsApi.handleCallback(mockCode);
      await fetchAccounts();
    } catch (e) {
      console.error('OAuth connection error', e);
    }
  };

  const handleDisconnect = async (accountId: string) => {
    try {
      await googleSheetsApi.disconnectAccount(accountId);
      if (selectedAccountId === accountId) {
        setSelectedAccountId(null);
      }
      await fetchAccounts();
    } catch (e) {
      console.error('Disconnect error', e);
    }
  };

  return {
    accounts,
    selectedAccountId,
    setSelectedAccountId,
    loading,
    handleConnect,
    handleDisconnect,
    refetchAccounts: fetchAccounts,
  };
}
