import React from 'react';
import { AssetIntegrity } from '../types/assets';

interface Props {
  integrity?: AssetIntegrity;
}

export const AssetIntegrityBadge: React.FC<Props> = ({ integrity }) => {
  if (!integrity) return null;
  const isHealthy = integrity.integrity_status === 'healthy';

  return (
    <span
      style={{
        background: isHealthy ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
        color: isHealthy ? '#10B981' : '#EF4444',
        border: `1px solid ${isHealthy ? '#10B981' : '#EF4444'}40`,
        borderRadius: '4px',
        padding: '2px 8px',
        fontSize: '0.75rem',
        fontWeight: 600,
      }}
    >
      {isHealthy ? '✅ SHA-256 Verified' : `⚠️ ${integrity.integrity_status}`}
    </span>
  );
};
