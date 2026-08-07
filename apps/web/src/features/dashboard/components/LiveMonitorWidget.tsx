import React from 'react';
import { LiveMonitorItem } from '../types/dashboard';

interface Props {
  monitors: LiveMonitorItem[];
}

export const LiveMonitorWidget: React.FC<Props> = ({ monitors }) => {
  return (
    <div style={{ background: '#1a1d24', border: '1px solid #374151', borderRadius: '8px', padding: '20px', color: '#fff', marginBottom: '24px' }}>
      <h3 style={{ margin: '0 0 16px 0', fontSize: '1.1rem' }}>⚡ Live Operational Queue Monitor</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '12px' }}>
        {monitors.map((item, idx) => (
          <div key={idx} style={{ background: '#111827', padding: '12px', borderRadius: '6px', border: '1px solid #374151' }}>
            <div style={{ fontWeight: 600, fontSize: '0.85rem', color: '#9ca3af', marginBottom: '4px' }}>{item.queue_name}</div>
            <div style={{ display: 'flex', gap: '16px', fontSize: '0.8rem' }}>
              <span>Active: <strong style={{ color: '#60a5fa' }}>{item.active_count}</strong></span>
              <span>Pending: <strong style={{ color: '#F59E0B' }}>{item.pending_count}</strong></span>
              <span>Failed: <strong style={{ color: item.failed_count > 0 ? '#EF4444' : '#10B981' }}>{item.failed_count}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
