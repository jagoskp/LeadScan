import React from 'react';
import { ColumnDiscoveryResponse } from '../types/googleSheets';

interface Props {
  discovery: ColumnDiscoveryResponse | null;
  loading: boolean;
  onRefresh: () => void;
}

export const ColumnMappingViewer: React.FC<Props> = ({ discovery, loading, onRefresh }) => {
  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600 }}>Dynamic Header Discovery & Schema</h3>
        <button
          onClick={onRefresh}
          style={{
            background: '#374151',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            padding: '6px 12px',
            fontSize: '0.85rem',
            cursor: 'pointer',
          }}
        >
          🔄 Refresh Headers
        </button>
      </div>

      {loading ? (
        <p style={{ color: '#9ca3af' }}>Reading sheet headers dynamically...</p>
      ) : !discovery ? (
        <p style={{ color: '#9ca3af' }}>Select a worksheet to discover headers.</p>
      ) : (
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '8px' }}>
          {discovery.discovered_headers.map((hdr, idx) => (
            <div
              key={idx}
              style={{
                background: '#111827',
                border: '1px solid #4b5563',
                borderRadius: '6px',
                padding: '6px 12px',
                fontSize: '0.85rem',
              }}
            >
              <span style={{ color: '#9ca3af', marginRight: '6px' }}>#{idx + 1}</span>
              <strong style={{ color: '#60a5fa' }}>{hdr}</strong>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
