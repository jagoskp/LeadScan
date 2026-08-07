import React from 'react';
import { Spreadsheet } from '../types/googleSheets';

interface Props {
  spreadsheets: Spreadsheet[];
  selectedSpreadsheetId: string | null;
  onSelectSpreadsheet: (spreadsheetId: string) => void;
  loading: boolean;
}

export const SpreadsheetBrowser: React.FC<Props> = ({
  spreadsheets,
  selectedSpreadsheetId,
  onSelectSpreadsheet,
  loading,
}) => {
  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '20px' }}>
      <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600, marginBottom: '12px' }}>Spreadsheet Discovery</h3>

      {loading ? (
        <p style={{ color: '#9ca3af' }}>Discovering spreadsheets from Google Drive...</p>
      ) : spreadsheets.length === 0 ? (
        <p style={{ color: '#9ca3af' }}>No spreadsheets found. Please select a connected Google Account.</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '12px' }}>
          {spreadsheets.map((sheet) => {
            const isSelected = sheet.id === selectedSpreadsheetId;
            return (
              <div
                key={sheet.id}
                onClick={() => onSelectSpreadsheet(sheet.id)}
                style={{
                  border: isSelected ? '2px solid #34A853' : '1px solid #374151',
                  background: isSelected ? 'rgba(52, 168, 83, 0.1)' : '#111827',
                  borderRadius: '6px',
                  padding: '12px',
                  cursor: 'pointer',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '1.2rem', color: '#34A853' }}>📊</span>
                  <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{sheet.title}</div>
                </div>
                <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '8px', wordBreak: 'break-all' }}>
                  ID: {sheet.id}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
