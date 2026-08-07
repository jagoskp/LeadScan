import { Lead, LeadTimelineItem } from '../types/leads';

const BASE_URL = '/api/v1/leads';

export const leadsApi = {
  async listLeads(search?: string, status?: string, isArchived: boolean = false): Promise<Lead[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (status) params.append('status', status);
    if (isArchived) params.append('is_archived', 'true');

    const res = await fetch(`${BASE_URL}?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch leads');
    return res.json();
  },

  async getLead(leadId: string): Promise<Lead> {
    const res = await fetch(`${BASE_URL}/${leadId}`);
    if (!res.ok) throw new Error('Failed to fetch lead details');
    return res.json();
  },

  async createLead(payload: Record<string, unknown>): Promise<Lead> {
    const res = await fetch(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to create lead');
    return res.json();
  },

  async updateLead(leadId: string, payload: Record<string, unknown>): Promise<Lead> {
    const res = await fetch(`${BASE_URL}/${leadId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to update lead');
    return res.json();
  },

  async archiveLead(leadId: string): Promise<Lead> {
    const res = await fetch(`${BASE_URL}/${leadId}/archive`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to archive lead');
    return res.json();
  },

  async restoreLead(leadId: string): Promise<Lead> {
    const res = await fetch(`${BASE_URL}/${leadId}/restore`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to restore lead');
    return res.json();
  },

  async mergeLeads(primaryLeadId: string, secondaryLeadIds: string[]): Promise<Lead> {
    const res = await fetch(`${BASE_URL}/merge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ primary_lead_id: primaryLeadId, secondary_lead_ids: secondaryLeadIds }),
    });
    if (!res.ok) throw new Error('Failed to merge leads');
    return res.json();
  },

  async getTimeline(leadId: string): Promise<LeadTimelineItem[]> {
    const res = await fetch(`${BASE_URL}/${leadId}/timeline`);
    if (!res.ok) throw new Error('Failed to fetch lead timeline');
    return res.json();
  },
};
