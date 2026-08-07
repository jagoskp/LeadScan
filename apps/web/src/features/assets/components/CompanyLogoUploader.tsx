import React from 'react';
import { useCompanyLogo } from '../hooks/useCompanyLogo';

interface Props {
  companyId: string;
}

export const CompanyLogoUploader: React.FC<Props> = ({ companyId }) => {
  const { logo, loading } = useCompanyLogo(companyId);

  if (loading) return <p style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Loading company logo...</p>;

  return (
    <div style={{ background: '#111827', border: '1px solid #374151', borderRadius: '6px', padding: '12px', color: '#fff', display: 'flex', alignItems: 'center', gap: '16px' }}>
      <div
        style={{
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: '#1f2937',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.5rem',
        }}
      >
        🏢
      </div>
      <div>
        <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>
          Company Logo {logo?.is_default && <span style={{ color: '#F59E0B', fontSize: '0.75rem', marginLeft: '6px' }}>(Default System Fallback)</span>}
        </div>
        <div style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{logo?.logo_url}</div>
      </div>
    </div>
  );
};
