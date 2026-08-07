import { useCallback, useEffect, useState } from 'react';
import { workspacesApi } from '../services/workspacesApi';
import { Organization, Workspace } from '../types/workspaces';

export function useWorkspaces() {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [selectedOrgId, setSelectedOrgId] = useState<string | null>(null);
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchOrgs = useCallback(async () => {
    setLoading(true);
    try {
      const orgs = await workspacesApi.listOrganizations();
      setOrganizations(orgs);
      if (orgs.length > 0 && !selectedOrgId) {
        setSelectedOrgId(orgs[0].id);
      }
    } catch (e) {
      console.error('Failed to load organizations', e);
    } finally {
      setLoading(false);
    }
  }, [selectedOrgId]);

  const fetchWorkspaces = useCallback(async () => {
    if (!selectedOrgId) return;
    try {
      const list = await workspacesApi.listWorkspaces(selectedOrgId);
      setWorkspaces(list);
    } catch (e) {
      console.error('Failed to load workspaces', e);
    }
  }, [selectedOrgId]);

  useEffect(() => {
    fetchOrgs();
  }, [fetchOrgs]);

  useEffect(() => {
    fetchWorkspaces();
  }, [fetchWorkspaces]);

  const createOrg = async (name: string) => {
    try {
      const newOrg = await workspacesApi.createOrganization(name);
      setOrganizations((prev) => [newOrg, ...prev]);
      setSelectedOrgId(newOrg.id);
    } catch (e) {
      console.error('Failed to create org', e);
    }
  };

  const createWorkspace = async (name: string) => {
    if (!selectedOrgId) return;
    try {
      const newWs = await workspacesApi.createWorkspace(selectedOrgId, name);
      setWorkspaces((prev) => [newWs, ...prev]);
    } catch (e) {
      console.error('Failed to create workspace', e);
    }
  };

  return {
    organizations,
    selectedOrgId,
    setSelectedOrgId,
    workspaces,
    loading,
    createOrg,
    createWorkspace,
    refetch: fetchOrgs,
  };
}
