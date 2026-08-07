import React from 'react';
import { Worksheet } from '../types/googleSheets';

interface Props {
  worksheets: Worksheet[];
  selectedWorksheetTitle: string | null;
  onSelectWorksheet: (title: string) => void;
  loading: boolean;
}

export const WorksheetSelector: React.FC<Props> = ({
  worksheets,
  selectedWorksheetTitle,
  onSelectWorksheet,
  loading,
}) => {
  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '20px' }}>
      <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600, marginBottom: '12px' }}>Worksheet Target Selection</h3>

      {loading ? (
        <p style={{ color: '#9ca3af' }}>Fetching worksheets...</p>
      ) : worksheets.length === 0 ? (
        <p style={{ color: '#9ca3af' }}>Select a spreadsheet first.</p>
      ) : (
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          {worksheets.map((ws) => {
            const isSelected = ws.title === selectedWorksheetTitle;
            return (
              <button
                key={ws.worksheet_id}
                onClick={() => onSelectWorksheet(ws.title)}
                style={{
                  background: isSelected ? '#34A853' : '#111827',
                  color: '#fff',
                  border: isSelected ? 'none' : '1px solid #374151',
                  borderRadius: '6px',
                  padding: '8px 16px',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                📄 {ws.title} ({ws.row_count} rows)
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};
