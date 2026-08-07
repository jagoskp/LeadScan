export interface Organization {
  id: string;
  name: string;
  logo_url?: string;
  timezone: string;
  status: string;
  created_at: string;
}

export interface Workspace {
  id: string;
  organization_id: string;
  name: string;
  is_default: boolean;
  created_at: string;
}

export interface Team {
  id: string;
  workspace_id: string;
  name: string;
  team_lead_id?: string;
}

export interface Invitation {
  id: string;
  organization_id: string;
  email: string;
  role_name: string;
  token: string;
  status: string;
  expires_at: string;
  created_at: string;
}

export interface Session {
  id: string;
  user_id: string;
  device_info: string;
  ip_address: string;
  is_active: boolean;
  last_active_at: string;
}
