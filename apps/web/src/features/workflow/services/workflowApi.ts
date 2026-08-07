import { FollowUp, SLA, Task, Workflow } from '../types/workflow';

const BASE_URL = '/api/v1/workflows';

export const workflowApi = {
  async listWorkflows(): Promise<Workflow[]> {
    const res = await fetch(BASE_URL);
    if (!res.ok) throw new Error('Failed to fetch workflows');
    return res.json();
  },

  async createWorkflow(name: string, triggerType: string): Promise<Workflow> {
    const res = await fetch(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, trigger_type: triggerType, is_active: true }),
    });
    if (!res.ok) throw new Error('Failed to create workflow');
    return res.json();
  },

  async listTasks(leadId?: string, status?: string): Promise<Task[]> {
    let url = `${BASE_URL}/tasks`;
    const params = new URLSearchParams();
    if (leadId) params.append('lead_id', leadId);
    if (status) params.append('status', status);
    if (params.toString()) url += `?${params.toString()}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return res.json();
  },

  async createTask(title: string, leadId?: string, priority: string = 'Medium'): Promise<Task> {
    const res = await fetch(`${BASE_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, lead_id: leadId, priority }),
    });
    if (!res.ok) throw new Error('Failed to create task');
    return res.json();
  },

  async completeTask(taskId: string): Promise<Task> {
    const res = await fetch(`${BASE_URL}/tasks/${taskId}/complete`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to complete task');
    return res.json();
  },

  async listFollowUps(leadId?: string): Promise<FollowUp[]> {
    let url = `${BASE_URL}/followups`;
    if (leadId) url += `?lead_id=${leadId}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch follow-ups');
    return res.json();
  },

  async scheduleFollowUp(
    leadId: string,
    followUpType: string,
    summary: string,
    scheduledAt: string
  ): Promise<FollowUp> {
    const res = await fetch(`${BASE_URL}/followups`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lead_id: leadId,
        follow_up_type: followUpType,
        summary,
        scheduled_at: scheduledAt,
      }),
    });
    if (!res.ok) throw new Error('Failed to schedule follow-up');
    return res.json();
  },
};
