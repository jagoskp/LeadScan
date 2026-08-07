import React from 'react';
import { LeadNote } from '../types/leads';

interface Props {
  notes: LeadNote[];
}

export const LeadNotesTab: React.FC<Props> = ({ notes }) => {
  if (!notes || notes.length === 0) {
    return <p style={{ color: '#9ca3af', fontSize: '0.85rem' }}>No notes recorded for this lead.</p>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {notes.map((n) => (
        <div key={n.id} style={{ background: '#111827', border: '1px solid #374151', borderRadius: '6px', padding: '10px', color: '#fff', fontSize: '0.85rem' }}>
          <div>{n.content}</div>
          <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '4px' }}>
            {new Date(n.created_at).toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  );
};
