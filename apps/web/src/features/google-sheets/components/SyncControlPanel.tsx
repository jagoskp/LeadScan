import React, { useState } from 'react';

interface Props {
  onExecuteSync: (syncMode: string) => void;
  syncing: boolean;
  disabled: boolean;
}

export const SyncControlPanel: React.FC<Props> = ({ onExecuteSync, syncing, disabled }) => {
  const [mode, setMode] = useState<string>('Manual');

  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '20px' }}>
      <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600, marginBottom: '12px' }}>Synchronization Control Panel</h3>

      <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
        <div>
          <label style={{ fontSize: '0.85rem', color: '#9ca3af', marginRight: '8px' }}>Sync Mode:</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            style={{
              background: '#111827',
              color: '#fff',
              border: '1px solid #374151',
              borderRadius: '4px',
              padding: '6px 12px',
            }}
          >
            <option value="Manual">Manual</option>
            <option value="Realtime">Realtime</option>
            <option value="Scheduled">Scheduled</option>
            <option value="Batch">Batch</option>
            <option value="Retry">Retry</option>
          </select>
        </div>

        <button
          disabled={disabled || syncing}
          onClick={() => onExecuteSync(mode)}
          style={{
            background: disabled ? '#4b5563' : 'linear-gradient(135deg, #34A853 0%, #0F9D58 100%)',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '10px 24px',
            fontWeight: 700,
            fontSize: '0.95rem',
            cursor: disabled || syncing ? 'not-allowed' : 'pointer',
          }}
        >
          {syncing ? 'Synchronizing...' : '🚀 Execute Synchronization'}
        </button>
      </div>
    </div>
  );
};
