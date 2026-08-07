import { Invitation, Organization, Session, Workspace } from '../types/workspaces';

const BASE_URL = '/api/v1/workspaces';

export const workspacesApi = {
  async listOrganizations(): Promise<Organization[]> {
    const res = await fetch(`${BASE_URL}/organizations`);
    if (!res.ok) throw new Error('Failed to fetch organizations');
    return res.json();
  },

  async createOrganization(name: string): Promise<Organization> {
    const res = await fetch(`${BASE_URL}/organizations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    if (!res.ok) throw new Error('Failed to create organization');
    return res.json();
  },

  async listWorkspaces(orgId: string): Promise<Workspace[]> {
    const res = await fetch(`${BASE_URL}?org_id=${orgId}`);
    if (!res.ok) throw new Error('Failed to fetch workspaces');
    return res.json();
  },

  async createWorkspace(orgId: string, name: string): Promise<Workspace> {
    const res = await fetch(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ organization_id: orgId, name }),
    });
    if (!res.ok) throw new Error('Failed to create workspace');
    return res.json();
  },

  async inviteUser(orgId: string, email: string, roleName: string = 'Viewer'): Promise<Invitation> {
    const res = await fetch(`${BASE_URL}/invite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ organization_id: orgId, email, role_name: roleName }),
    });
    if (!res.ok) throw new Error('Failed to send invitation');
    return res.json();
  },

  async listActiveSessions(userId: string): Promise<Session[]> {
    const res = await fetch(`${BASE_URL}/sessions?user_id=${userId}`);
    if (!res.ok) throw new Error('Failed to fetch sessions');
    return res.json();
  },

  async forceLogoutSession(sessionId: string): Promise<boolean> {
    const res = await fetch(`${BASE_URL}/sessions/${sessionId}/logout`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to logout session');
    const data = await res.json();
    return data.success;
  },
};
