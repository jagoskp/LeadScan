import {
  DuplicateMatch,
  MergeHistory,
  MergePreviewResponse,
  RollbackHistory,
} from '../types/identity';

const BASE_URL = '/api/v1/identity';

export const identityApi = {
  async listDuplicateMatches(statusFilter: string = 'pending'): Promise<DuplicateMatch[]> {
    const res = await fetch(`${BASE_URL}/duplicates?status=${statusFilter}`);
    if (!res.ok) throw new Error('Failed to fetch duplicate matches');
    return res.json();
  },

  async scanForDuplicates(): Promise<DuplicateMatch[]> {
    const res = await fetch(`${BASE_URL}/scan`, { method: 'POST' });
    if (!res.ok) throw new Error('Duplicate scan failed');
    return res.json();
  },

  async getMergePreview(primaryLeadId: string, secondaryLeadId: string): Promise<MergePreviewResponse> {
    const res = await fetch(
      `${BASE_URL}/merge-preview?primary_lead_id=${primaryLeadId}&secondary_lead_id=${secondaryLeadId}`
    );
    if (!res.ok) throw new Error('Failed to load merge preview');
    return res.json();
  },

  async executeMerge(
    primaryLeadId: string,
    secondaryLeadIds: string[],
    policy: string = 'keep_original'
  ): Promise<MergeHistory> {
    const res = await fetch(`${BASE_URL}/merge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        primary_lead_id: primaryLeadId,
        secondary_lead_ids: secondaryLeadIds,
        resolution_policy: policy,
      }),
    });
    if (!res.ok) throw new Error('Merge execution failed');
    return res.json();
  },

  async rollbackMerge(mergeHistoryId: string): Promise<RollbackHistory> {
    const res = await fetch(`${BASE_URL}/rollback/${mergeHistoryId}`, { method: 'POST' });
    if (!res.ok) throw new Error('Rollback failed');
    return res.json();
  },
};
