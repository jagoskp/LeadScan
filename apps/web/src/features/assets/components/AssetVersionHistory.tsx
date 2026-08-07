import React from 'react';
import { AssetVersion } from '../types/assets';

interface Props {
  versions: AssetVersion[];
  onRollback: (versionNumber: number) => void;
  isImmutable: boolean;
}

export const AssetVersionHistory: React.FC<Props> = ({ versions, onRollback, isImmutable }) => {
  if (!versions || versions.length === 0) return <p style={{ color: '#9ca3af', fontSize: '0.85rem' }}>No version history.</p>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {versions.map((v) => (
        <div
          key={v.id}
          style={{
            background: '#111827',
            border: '1px solid #374151',
            borderRadius: '6px',
            padding: '10px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            color: '#fff',
            fontSize: '0.85rem',
          }}
        >
          <div>
            <strong>Version {v.version_number}</strong>
            <div style={{ fontSize: '0.75rem', color: '#9ca3af' }}>
              SHA256: {v.checksum_sha256.substring(0, 16)}...
            </div>
          </div>

          {!isImmutable && (
            <button
              onClick={() => onRollback(v.version_number)}
              style={{
                background: '#374151',
                color: '#60a5fa',
                border: 'none',
                borderRadius: '4px',
                padding: '4px 10px',
                cursor: 'pointer',
                fontSize: '0.8rem',
              }}
            >
              ⏪ Rollback
            </button>
          )}
        </div>
      ))}
    </div>
  );
};
