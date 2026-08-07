// Types for the Universal Connector Studio (BF-010)

export type ConnectorHealthStatus =
  | "Healthy"
  | "Warning"
  | "Disconnected"
  | "Expired"
  | "Authentication Failed"
  | "Rate Limited"
  | "Maintenance";

export type ConnectorPermissionType = "Read" | "Write" | "Admin";

export interface ConnectorDriver {
  id: string;
  name: string;
  connector_type: string;
  version: string;
  is_active: boolean;
  created_at: string;
}

export interface ConnectorAccount {
  id: string;
  connector_id: string;
  user_id: string | null;
  organization_id: string | null;
  account_email: string;
  account_label: string | null;
  is_default: boolean;
  created_at: string;
}

export interface ConnectorCredential {
  id: string;
  connection_id: string;
  encrypted_token: string;
  refresh_token: string | null;
  expires_at: string | null;
  created_at: string;
}

export interface ConnectorHealth {
  id: string;
  connection_id: string;
  status: ConnectorHealthStatus;
  last_checked: string;
  latency_ms: number | null;
  error_message: string | null;
}

export interface ConnectorAudit {
  id: string;
  connection_id: string;
  user_id: string | null;
  action: string;
  details: string | null;
  created_at: string;
}

export interface ConnectorPermission {
  id: string;
  connection_id: string;
  user_id: string | null;
  permission_type: ConnectorPermissionType;
  created_at: string;
}

export interface ConnectorConnection {
  id: string;
  account_id: string;
  name: string;
  is_enabled: boolean;
  labels: string[];
  tags: string[];
  credentials: ConnectorCredential[];
  health_records: ConnectorHealth[];
  audit_logs: ConnectorAudit[];
  permissions: ConnectorPermission[];
  created_at: string;
}
