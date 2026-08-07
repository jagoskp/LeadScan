import React from 'react';
import { getConfidenceColor } from '../utils/identityUtils';

interface Props {
  level: string;
}

export const ConfidenceBadge: React.FC<Props> = ({ level }) => {
  const color = getConfidenceColor(level);
  return (
    <span
      style={{
        background: `${color}20`,
        color: color,
        border: `1px solid ${color}40`,
        borderRadius: '4px',
        padding: '2px 8px',
        fontSize: '0.8rem',
        fontWeight: 700,
      }}
    >
      {level} Confidence
    </span>
  );
};
