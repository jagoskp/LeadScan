import React from 'react';
import { getRoleBadgeColor } from '../utils/workspaceUtils';

export const RolePermissionMatrix: React.FC = () => {
  const roles = [
    { name: 'Owner', desc: 'Full organization ownership, billing, & tenant control' },
    { name: 'Admin', desc: 'Organization administration & workspace configuration' },
    { name: 'Manager', desc: 'Team lead, task assignment, & SLA management' },
    { name: 'Operator', desc: 'Lead creation, Google Sync, & asset management' },
    { name: 'Reviewer', desc: 'Review Workspace approval & OCR verification' },
    { name: 'Viewer', desc: 'Read-only access to master repository' },
  ];

  return (
    <div style={{ background: '#1a1d24', border: '1px solid #374151', borderRadius: '8px', padding: '20px', color: '#fff', marginBottom: '24px' }}>
      <h3 style={{ margin: '0 0 16px 0', fontSize: '1.1rem' }}>🔐 Role-Based Access Control (RBAC) Matrix</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '12px' }}>
        {roles.map((r, idx) => {
          const color = getRoleBadgeColor(r.name);
          return (
            <div key={idx} style={{ background: '#111827', padding: '12px', borderRadius: '6px', border: '1px solid #374151' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <span style={{ background: `${color}20`, color, fontSize: '0.8rem', fontWeight: 700, padding: '2px 8px', borderRadius: '4px' }}>
                  {r.name}
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: '#9ca3af', margin: 0 }}>{r.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
