import React from 'react';
import { Organization } from '../types/workspaces';

interface Props {
  organizations: Organization[];
  selectedOrgId: string | null;
  onSelectOrg: (id: string) => void;
  onCreateOrg: (name: string) => void;
}

export const OrganizationSwitcher: React.FC<Props> = ({
  organizations,
  selectedOrgId,
  onSelectOrg,
  onCreateOrg,
}) => {
  return (
    <div style={{ background: '#1a1d24', border: '1px solid #374151', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontWeight: 700 }}>ACTIVE ORGANIZATION TENANT</span>
          <select
            value={selectedOrgId || ''}
            onChange={(e) => onSelectOrg(e.target.value)}
            style={{
              display: 'block',
              marginTop: '4px',
              background: '#111827',
              color: '#fff',
              border: '1px solid #374151',
              borderRadius: '6px',
              padding: '8px 12px',
              fontSize: '1rem',
              fontWeight: 600,
            }}
          >
            {organizations.map((org) => (
              <option key={org.id} value={org.id}>
                🏢 {org.name} ({org.status.toUpperCase()})
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={() => {
            const name = prompt('Enter New Organization Name:');
            if (name) onCreateOrg(name);
          }}
          style={{
            background: '#3B82F6',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 16px',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          + Create Organization
        </button>
      </div>
    </div>
  );
};
