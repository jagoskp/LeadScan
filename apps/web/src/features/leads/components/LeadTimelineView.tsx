import React from 'react';
import { useLeadTimeline } from '../hooks/useLeadTimeline';

interface Props {
  leadId: string;
}

export const LeadTimelineView: React.FC<Props> = ({ leadId }) => {
  const { timeline, loading } = useLeadTimeline(leadId);

  if (loading) return <p style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Loading timeline events...</p>;
  if (timeline.length === 0) return <p style={{ color: '#9ca3af', fontSize: '0.85rem' }}>No audit timeline items.</p>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', borderLeft: '2px solid #374151', paddingLeft: '16px' }}>
      {timeline.map((item) => (
        <div key={item.id} style={{ position: 'relative' }}>
          <div
            style={{
              position: 'absolute',
              left: '-23px',
              top: '2px',
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              background: '#3B82F6',
            }}
          />
          <div style={{ fontWeight: 600, fontSize: '0.85rem', color: '#60a5fa' }}>{item.title}</div>
          <div style={{ fontSize: '0.8rem', color: '#d1d5db' }}>{item.description}</div>
          <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '2px' }}>
            {new Date(item.created_at).toLocaleString()} • Event: {item.event_type}
          </div>
        </div>
      ))}
    </div>
  );
};
