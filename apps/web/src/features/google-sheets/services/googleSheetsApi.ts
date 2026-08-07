import {
  ColumnDiscoveryResponse,
  GoogleAccount,
  MappingValidationReport,
  Spreadsheet,
  SyncHistoryItem,
  SyncJob,
  Worksheet,
} from '../types/googleSheets';

const BASE_URL = '/api/v1/google-connector';

export const googleSheetsApi = {
  async getAuthUrl(): Promise<{ authorization_url: string; state: string }> {
    const res = await fetch(`${BASE_URL}/oauth/auth-url`);
    if (!res.ok) throw new Error('Failed to fetch OAuth URL');
    return res.json();
  },

  async handleCallback(code: string, state?: string): Promise<{ account_id: string; account_email: string }> {
    const res = await fetch(`${BASE_URL}/oauth/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, state }),
    });
    if (!res.ok) throw new Error('OAuth Callback exchange failed');
    return res.json();
  },

  async getAccounts(): Promise<GoogleAccount[]> {
    const res = await fetch(`${BASE_URL}/accounts`);
    if (!res.ok) throw new Error('Failed to list Google Accounts');
    return res.json();
  },

  async disconnectAccount(accountId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/accounts/${accountId}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to disconnect account');
  },

  async getSpreadsheets(accountId: string): Promise<Spreadsheet[]> {
    const res = await fetch(`${BASE_URL}/spreadsheets?account_id=${accountId}`);
    if (!res.ok) throw new Error('Failed to discover spreadsheets');
    return res.json();
  },

  async getWorksheets(accountId: string, spreadsheetId: string): Promise<Worksheet[]> {
    const res = await fetch(`${BASE_URL}/worksheets?account_id=${accountId}&spreadsheet_id=${spreadsheetId}`);
    if (!res.ok) throw new Error('Failed to discover worksheets');
    return res.json();
  },

  async getColumns(
    accountId: string,
    spreadsheetId: string,
    worksheetTitle: string
  ): Promise<ColumnDiscoveryResponse> {
    const res = await fetch(
      `${BASE_URL}/columns?account_id=${accountId}&spreadsheet_id=${spreadsheetId}&worksheet_title=${encodeURIComponent(
        worksheetTitle
      )}`
    );
    if (!res.ok) throw new Error('Failed to discover columns');
    return res.json();
  },

  async preSyncCheck(
    accountId: string,
    profileId: string,
    spreadsheetId: string,
    worksheetTitle: string
  ): Promise<MappingValidationReport> {
    const res = await fetch(`${BASE_URL}/pre-sync-check?account_id=${accountId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profile_id: profileId,
        spreadsheet_id: spreadsheetId,
        worksheet_title: worksheetTitle,
      }),
    });
    if (!res.ok) throw new Error('Pre-sync validation failed');
    return res.json();
  },

  async executeSync(
    accountId: string,
    payload: {
      profile_id: string;
      spreadsheet_id: string;
      worksheet_title: string;
      sync_mode: string;
      rows_data: Record<string, unknown>[];
      auto_apply_remapping?: boolean;
    }
  ): Promise<SyncJob> {
    const res = await fetch(`${BASE_URL}/sync?account_id=${accountId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Sync execution failed');
    return res.json();
  },

  async getHistory(): Promise<SyncHistoryItem[]> {
    const res = await fetch(`${BASE_URL}/history`);
    if (!res.ok) throw new Error('Failed to fetch sync history');
    return res.json();
  },
};
