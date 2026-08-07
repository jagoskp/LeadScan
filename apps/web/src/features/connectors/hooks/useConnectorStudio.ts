"use client";

import { useState, useEffect, useCallback } from "react";
import type { ConnectorConnection, ConnectorDriver } from "../types/connector";
import {
  fetchDrivers,
  fetchConnections,
  testConnection,
  checkConnectionHealth,
  refreshConnectionTokens,
  deleteConnection,
} from "../services/api";

interface ConnectorStudioState {
  drivers: ConnectorDriver[];
  connections: ConnectorConnection[];
  selectedConnection: ConnectorConnection | null;
  isLoading: boolean;
  error: string | null;
}

export function useConnectorStudio() {
  const [state, setState] = useState<ConnectorStudioState>({
    drivers: [],
    connections: [],
    selectedConnection: null,
    isLoading: false,
    error: null,
  });

  const load = useCallback(async () => {
    setState((s) => ({ ...s, isLoading: true, error: null }));
    try {
      const [drivers, connections] = await Promise.all([
        fetchDrivers(),
        fetchConnections(),
      ]);
      setState((s) => ({ ...s, drivers, connections, isLoading: false }));
    } catch (err) {
      setState((s) => ({
        ...s,
        isLoading: false,
        error: err instanceof Error ? err.message : "Unknown error",
      }));
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const selectConnection = useCallback(
    (connection: ConnectorConnection | null) => {
      setState((s) => ({ ...s, selectedConnection: connection }));
    },
    []
  );

  const handleTest = useCallback(async (id: string) => {
    return testConnection(id);
  }, []);

  const handleHealthCheck = useCallback(async (id: string) => {
    return checkConnectionHealth(id);
  }, []);

  const handleRefresh = useCallback(async (id: string) => {
    return refreshConnectionTokens(id);
  }, []);

  const handleDelete = useCallback(
    async (id: string) => {
      await deleteConnection(id);
      await load();
    },
    [load]
  );

  return {
    ...state,
    selectConnection,
    handleTest,
    handleHealthCheck,
    handleRefresh,
    handleDelete,
    reload: load,
  };
}
