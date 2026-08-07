// Formatter helpers for the Connector Studio

import type { ConnectorHealthStatus } from "../types/connector";

export function formatHealthBadgeColor(status: ConnectorHealthStatus): string {
  const map: Record<ConnectorHealthStatus, string> = {
    Healthy: "#22c55e",
    Warning: "#f59e0b",
    Disconnected: "#6b7280",
    Expired: "#ef4444",
    "Authentication Failed": "#dc2626",
    "Rate Limited": "#f97316",
    Maintenance: "#8b5cf6",
  };
  return map[status] ?? "#6b7280";
}

export function formatConnectionLabel(
  name: string,
  labels: string[]
): string {
  return labels.length > 0 ? `${name} [${labels.join(", ")}]` : name;
}
