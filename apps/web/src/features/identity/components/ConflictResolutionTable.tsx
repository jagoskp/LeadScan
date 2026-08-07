import React from 'react';
import { MergeConflict } from '../types/identity';

interface Props {
  conflicts: MergeConflict[];
}

export const ConflictResolutionTable: React.FC<Props> = ({ conflicts }) => {
  if (!conflicts || conflicts.length === 0) {
    return <p style={{ color: '#10B981', fontSize: '0.85rem' }}>✅ No field conflicts detected between primary and secondary records.</p>;
  }

  return (
    <div style={{ background: '#111827', borderRadius: '6px', overflow: 'hidden', margin: '12px 0' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', color: '#fff', fontSize: '0.85rem' }}>
        <thead>
          <tr style={{ background: '#1f2937', color: '#9ca3af', textAlign: 'left', borderBottom: '1px solid #374151' }}>
            <th style={{ padding: '8px 12px' }}>Field Name</th>
            <th style={{ padding: '8px 12px' }}>Primary Value</th>
            <th style={{ padding: '8px 12px' }}>Secondary Value</th>
            <th style={{ padding: '8px 12px' }}>Resolved Choice</th>
          </tr>
        </thead>
        <tbody>
          {conflicts.map((c, idx) => (
            <tr key={idx} style={{ borderBottom: '1px solid #374151' }}>
              <td style={{ padding: '8px 12px', fontWeight: 600, color: '#60a5fa' }}>{c.field_name}</td>
              <td style={{ padding: '8px 12px', color: '#d1d5db' }}>{c.primary_value || 'None'}</td>
              <td style={{ padding: '8px 12px', color: '#d1d5db' }}>{c.secondary_value || 'None'}</td>
              <td style={{ padding: '8px 12px', color: '#10B981', fontWeight: 600 }}>{c.resolved_value || 'Original'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
