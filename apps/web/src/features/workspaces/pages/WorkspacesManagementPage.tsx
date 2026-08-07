import React from 'react';
import { OrganizationSwitcher } from '../components/OrganizationSwitcher';
import { RolePermissionMatrix } from '../components/RolePermissionMatrix';
import { useWorkspaces } from '../hooks/useWorkspaces';

export const WorkspacesManagementPage: React.FC = () => {
  const {
    organizations,
    selectedOrgId,
    setSelectedOrgId,
    workspaces,
    loading,
    createOrg,
    createWorkspace,
  } = useWorkspaces();

  return (
    <div
      style={{
        padding: '32px',
        background: '#0f1117',
        minHeight: '100vh',
        color: '#fff',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Enterprise Multi-Workspace Platform</h1>
        <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
          Multi-tenant data isolation, workspace management, RBAC role permissions, tokenized invitations, and active sessions.
        </p>
      </div>

      <OrganizationSwitcher
        organizations={organizations}
        selectedOrgId={selectedOrgId}
        onSelectOrg={setSelectedOrgId}
        onCreateOrg={createOrg}
      />

      <RolePermissionMatrix />

      <div style={{ background: '#1a1d24', border: '1px solid #374151', borderRadius: '8px', padding: '20px', color: '#fff' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '1.1rem' }}>📁 Isolated Tenant Workspaces</h3>
          <button
            onClick={() => {
              const name = prompt('Enter Workspace Name:');
              if (name) createWorkspace(name);
            }}
            style={{ background: '#10B981', color: '#fff', border: 'none', borderRadius: '6px', padding: '8px 16px', fontWeight: 600, cursor: 'pointer' }}
          >
            + Create Workspace
          </button>
        </div>

        {loading ? (
          <p style={{ color: '#9ca3af' }}>Loading workspaces...</p>
        ) : workspaces.length === 0 ? (
          <p style={{ color: '#9ca3af' }}>No workspaces configured for this organization.</p>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '12px' }}>
            {workspaces.map((ws) => (
              <div key={ws.id} style={{ background: '#111827', border: '1px solid #374151', borderRadius: '6px', padding: '16px' }}>
                <div style={{ fontWeight: 700, fontSize: '1rem', color: '#60a5fa' }}>{ws.name}</div>
                {ws.is_default && <span style={{ fontSize: '0.7rem', color: '#10B981', fontWeight: 700 }}>DEFAULT WORKSPACE</span>}
                <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '6px' }}>ID: {ws.id.substring(0, 13)}...</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkspacesManagementPage;
