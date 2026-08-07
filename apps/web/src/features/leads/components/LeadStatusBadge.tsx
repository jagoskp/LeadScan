import React from 'react';
import { getStatusColor } from '../utils/leadUtils';

interface Props {
  status: string;
}

export const LeadStatusBadge: React.FC<Props> = ({ status }) => {
  const color = getStatusColor(status);
  return (
    <span
      style={{
        background: `${color}20`,
        color: color,
        border: `1px solid ${color}40`,
        borderRadius: '4px',
        padding: '2px 8px',
        fontSize: '0.8rem',
        fontWeight: 600,
      }}
    >
      {status}
    </span>
  );
};
