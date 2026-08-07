import React from 'react';
import { SearchFilterOptions } from '../types/search';

interface Props {
  filters: SearchFilterOptions;
  onChangeFilters: (newFilters: SearchFilterOptions) => void;
}

export const SearchFilterPanel: React.FC<Props> = ({ filters, onChangeFilters }) => {
  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '20px' }}>
      <h4 style={{ margin: '0 0 12px 0', fontSize: '0.95rem', color: '#60a5fa' }}>🎛️ Dynamic Search Filters</h4>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
        <div>
          <label style={{ fontSize: '0.75rem', color: '#9ca3af', display: 'block', marginBottom: '4px' }}>Lead Status</label>
          <select
            value={filters.status || ''}
            onChange={(e) => onChangeFilters({ ...filters, status: e.target.value || undefined })}
            style={{ width: '100%', background: '#111827', color: '#fff', border: '1px solid #374151', borderRadius: '4px', padding: '6px 8px' }}
          >
            <option value="">All Statuses</option>
            <option value="New">New</option>
            <option value="Contacted">Contacted</option>
            <option value="Qualified">Qualified</option>
            <option value="Won">Won</option>
            <option value="Lost">Lost</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.75rem', color: '#9ca3af', display: 'block', marginBottom: '4px' }}>Company Name</label>
          <input
            type="text"
            placeholder="Filter company..."
            value={filters.company_name || ''}
            onChange={(e) => onChangeFilters({ ...filters, company_name: e.target.value || undefined })}
            style={{ width: '100%', background: '#111827', color: '#fff', border: '1px solid #374151', borderRadius: '4px', padding: '6px 8px' }}
          />
        </div>

        <div>
          <label style={{ fontSize: '0.75rem', color: '#9ca3af', display: 'block', marginBottom: '4px' }}>Source Type</label>
          <select
            value={filters.source_type || ''}
            onChange={(e) => onChangeFilters({ ...filters, source_type: e.target.value || undefined })}
            style={{ width: '100%', background: '#111827', color: '#fff', border: '1px solid #374151', borderRadius: '4px', padding: '6px 8px' }}
          >
            <option value="">All Sources</option>
            <option value="Lead Repository">Lead Repository</option>
            <option value="OCR Result">OCR Result</option>
            <option value="Document">Document</option>
          </select>
        </div>
      </div>
    </div>
  );
};
