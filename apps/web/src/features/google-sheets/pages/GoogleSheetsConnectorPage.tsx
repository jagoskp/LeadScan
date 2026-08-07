import React, { useState } from 'react';
import { AutoRemappingModal } from '../components/AutoRemappingModal';
import { ColumnMappingViewer } from '../components/ColumnMappingViewer';
import { GoogleAccountSelector } from '../components/GoogleAccountSelector';
import { SpreadsheetBrowser } from '../components/SpreadsheetBrowser';
import { SyncControlPanel } from '../components/SyncControlPanel';
import { SyncHistoryTable } from '../components/SyncHistoryTable';
import { ValidationReportModal } from '../components/ValidationReportModal';
import { WorksheetSelector } from '../components/WorksheetSelector';
import { useColumnDiscovery } from '../hooks/useColumnDiscovery';
import { useGoogleOAuth } from '../hooks/useGoogleOAuth';
import { useGoogleSync } from '../hooks/useGoogleSync';
import { useSpreadsheetDiscovery } from '../hooks/useSpreadsheetDiscovery';

export const GoogleSheetsConnectorPage: React.FC = () => {
  const {
    accounts,
    selectedAccountId,
    setSelectedAccountId,
    handleConnect,
    handleDisconnect,
  } = useGoogleOAuth();

  const {
    spreadsheets,
    worksheets,
    selectedSpreadsheetId,
    setSelectedSpreadsheetId,
    selectedWorksheetTitle,
    setSelectedWorksheetTitle,
    loadingSpreadsheets,
    loadingWorksheets,
  } = useSpreadsheetDiscovery(selectedAccountId);

  const { discovery, loading: loadingColumns, refetchColumns } = useColumnDiscovery(
    selectedAccountId,
    selectedSpreadsheetId,
    selectedWorksheetTitle
  );

  const {
    history,
    validationReport,
    syncing,
    loadingHistory,
    runPreSyncCheck,
    executeSync,
  } = useGoogleSync(selectedAccountId, selectedSpreadsheetId, selectedWorksheetTitle);

  const [isValidationModalOpen, setIsValidationModalOpen] = useState<boolean>(false);
  const [isRemappingModalOpen, setIsRemappingModalOpen] = useState<boolean>(false);

  // Mock profile ID from BF-006 / BF-007
  const mockProfileId = '00000000-0000-0000-0000-000000000001';

  // Mock approved DOM rows from BF-008 Review Workspace
  const sampleDataToSync = [
    {
      'Business Name': 'Acme Enterprise Corp',
      'Email': 'contact@acme.com',
      'Phone Number': '+1 555 019 2831',
      'Contact Person': 'Jane Doe',
    },
    {
      'Business Name': 'Global Logistics Inc',
      'Email': 'info@globallogistics.com',
      'Phone Number': '+1 555 012 9948',
      'Contact Person': 'John Smith',
    },
  ];

  const handleTriggerSync = async (syncMode: string) => {
    // Step 1: Pre-sync Check
    const report = await runPreSyncCheck(mockProfileId);
    if (report && report.status !== 'Valid') {
      setIsValidationModalOpen(true);
      return;
    }

    // Step 2: Execute Sync
    try {
      await executeSync(mockProfileId, syncMode, sampleDataToSync, true);
    } catch (e) {
      console.error('Sync failed', e);
    }
  };

  return (
    <div
      style={{
        padding: '32px',
        background: '#0f1117',
        minHeight: '100vh',
        color: '#fff',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Google Sheets Production Connector</h1>
        <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
          Enterprise real-time & batch synchronization engine powered by Dynamic Mapping Profile (BF-006 / BF-007) and Secret Vault (BF-011).
        </p>
      </div>

      <GoogleAccountSelector
        accounts={accounts}
        selectedAccountId={selectedAccountId}
        onSelectAccount={setSelectedAccountId}
        onConnectAccount={handleConnect}
        onDisconnectAccount={handleDisconnect}
      />

      <SpreadsheetBrowser
        spreadsheets={spreadsheets}
        selectedSpreadsheetId={selectedSpreadsheetId}
        onSelectSpreadsheet={setSelectedSpreadsheetId}
        loading={loadingSpreadsheets}
      />

      <WorksheetSelector
        worksheets={worksheets}
        selectedWorksheetTitle={selectedWorksheetTitle}
        onSelectWorksheet={setSelectedWorksheetTitle}
        loading={loadingWorksheets}
      />

      <ColumnMappingViewer discovery={discovery} loading={loadingColumns} onRefresh={refetchColumns} />

      <SyncControlPanel
        onExecuteSync={handleTriggerSync}
        syncing={syncing}
        disabled={!selectedAccountId || !selectedSpreadsheetId || !selectedWorksheetTitle}
      />

      <SyncHistoryTable history={history} loading={loadingHistory} />

      <ValidationReportModal
        report={validationReport}
        isOpen={isValidationModalOpen}
        onClose={() => setIsValidationModalOpen(false)}
        onProceedWithRemapping={() => {
          setIsValidationModalOpen(false);
          setIsRemappingModalOpen(true);
        }}
      />

      <AutoRemappingModal
        suggestions={validationReport?.suggestions || []}
        isOpen={isRemappingModalOpen}
        onClose={() => setIsRemappingModalOpen(false)}
        onApplyRemapping={async () => {
          setIsRemappingModalOpen(false);
          await executeSync(mockProfileId, 'Manual', sampleDataToSync, true);
        }}
      />
    </div>
  );
};

export default GoogleSheetsConnectorPage;
