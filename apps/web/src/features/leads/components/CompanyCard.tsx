import React from 'react';
import { Company } from '../types/leads';

interface Props {
  company?: Company;
}

export const CompanyCard: React.FC<Props> = ({ company }) => {
  if (!company) {
    return (
      <div style={{ background: '#111827', borderRadius: '6px', padding: '12px', color: '#9ca3af', fontSize: '0.85rem' }}>
        No company details associated with this lead.
      </div>
    );
  }

  return (
    <div style={{ background: '#111827', border: '1px solid #374151', borderRadius: '6px', padding: '16px', color: '#fff' }}>
      <div style={{ fontWeight: 700, fontSize: '1rem', color: '#60a5fa', marginBottom: '8px' }}>
        🏢 {company.company_name}
      </div>
      <div style={{ fontSize: '0.85rem', color: '#d1d5db', display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {company.gst_number && <div><strong>GST:</strong> {company.gst_number}</div>}
        {company.industry && <div><strong>Industry:</strong> {company.industry}</div>}
        {company.website && <div><strong>Website:</strong> <a href={company.website} target="_blank" rel="noreferrer" style={{ color: '#3b82f6' }}>{company.website}</a></div>}
        {company.address && <div><strong>Address:</strong> {company.address}</div>}
      </div>
    </div>
  );
};
