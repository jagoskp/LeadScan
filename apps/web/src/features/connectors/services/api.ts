// API service bindings for the Connector Studio

import type {
  ConnectorAccount,
  ConnectorConnection,
  ConnectorDriver,
} from "../types/connector";

const BASE = "/api/connectors-studio";

export async function fetchDrivers(): Promise<ConnectorDriver[]> {
  const res = await fetch(`${BASE}/drivers`);
  if (!res.ok) throw new Error("Failed to fetch connector drivers");
  return res.json();
}

export async function fetchAccounts(): Promise<ConnectorAccount[]> {
  const res = await fetch(`${BASE}/accounts`);
  if (!res.ok) throw new Error("Failed to fetch connector accounts");
  return res.json();
}

export async function fetchConnections(): Promise<ConnectorConnection[]> {
  const res = await fetch(`${BASE}/connections`);
  if (!res.ok) throw new Error("Failed to fetch connections");
  return res.json();
}

export async function fetchConnectionById(
  id: string
): Promise<ConnectorConnection> {
  const res = await fetch(`${BASE}/connections/${id}`);
  if (!res.ok) throw new Error("Failed to fetch connection");
  return res.json();
}

export async function testConnection(id: string): Promise<{ success: boolean }> {
  const res = await fetch(`${BASE}/connections/${id}/test`, { method: "POST" });
  if (!res.ok) throw new Error("Connection test failed");
  return res.json();
}

export async function checkConnectionHealth(
  id: string
): Promise<{ health_status: string }> {
  const res = await fetch(`${BASE}/connections/${id}/health`, { method: "POST" });
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function refreshConnectionTokens(
  id: string
): Promise<{ success: boolean }> {
  const res = await fetch(`${BASE}/connections/${id}/refresh`, { method: "POST" });
  if (!res.ok) throw new Error("Token refresh failed");
  return res.json();
}

export async function deleteConnection(id: string): Promise<void> {
  const res = await fetch(`${BASE}/connections/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete connection");
}
