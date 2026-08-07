import React from 'react';
import { SystemHealthItem } from '../types/dashboard';

interface Props {
  healthItems: SystemHealthItem[];
}

export const SystemHealthWidget: React.FC<Props> = ({ healthItems }) => {
  return (
    <div style={{ background: '#1a1d24', border: '1px solid #374151', borderRadius: '8px', padding: '20px', color: '#fff' }}>
      <h3 style={{ margin: '0 0 16px 0', fontSize: '1.1rem' }}>🛡️ System Telemetry & Component Health</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {healthItems.map((item, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#111827', padding: '10px 14px', borderRadius: '6px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ height: '8px', width: '8px', borderRadius: '50%', background: item.status === 'operational' ? '#10B981' : '#F59E0B' }} />
              <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{item.component}</span>
            </div>
            <div style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
              Latency: <strong style={{ color: '#10B981' }}>{item.latency_ms} ms</strong>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
