import React from 'react';
import { SyncHistoryItem } from '../types/googleSheets';

interface Props {
  history: SyncHistoryItem[];
  loading: boolean;
}

export const SyncHistoryTable: React.FC<Props> = ({ history, loading }) => {
  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff' }}>
      <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600, marginBottom: '12px' }}>Sync Execution History</h3>

      {loading ? (
        <p style={{ color: '#9ca3af' }}>Loading history logs...</p>
      ) : history.length === 0 ? (
        <p style={{ color: '#9ca3af' }}>No sync execution records found.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #374151', color: '#9ca3af', textAlign: 'left' }}>
              <th style={{ padding: '8px' }}>Job ID</th>
              <th style={{ padding: '8px' }}>Spreadsheet / Sheet</th>
              <th style={{ padding: '8px' }}>Rows</th>
              <th style={{ padding: '8px' }}>Duration</th>
              <th style={{ padding: '8px' }}>Status</th>
              <th style={{ padding: '8px' }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr key={item.id} style={{ borderBottom: '1px solid #1f2937' }}>
                <td style={{ padding: '8px', fontFamily: 'monospace' }}>{item.job_id.substring(0, 8)}...</td>
                <td style={{ padding: '8px' }}>
                  {item.spreadsheet_id.substring(0, 10)}... / {item.worksheet_id}
                </td>
                <td style={{ padding: '8px' }}>{item.rows_processed}</td>
                <td style={{ padding: '8px' }}>{item.duration_ms} ms</td>
                <td style={{ padding: '8px' }}>
                  <span
                    style={{
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: item.status === 'Success' ? 'rgba(52, 168, 83, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                      color: item.status === 'Success' ? '#34A853' : '#ef4444',
                      fontWeight: 600,
                    }}
                  >
                    {item.status}
                  </span>
                </td>
                <td style={{ padding: '8px', color: '#9ca3af' }}>
                  {new Date(item.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
