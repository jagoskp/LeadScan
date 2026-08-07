export interface Task {
  id: string;
  lead_id?: string;
  title: string;
  description?: string;
  priority: string;
  status: string;
  due_date?: string;
  assignee_id?: string;
  created_at: string;
}

export interface FollowUp {
  id: string;
  lead_id: string;
  follow_up_type: string;
  summary: string;
  notes?: string;
  scheduled_at: string;
  completed_at?: string;
  is_completed: boolean;
  created_at: string;
}

export interface WorkflowRule {
  id: string;
  workflow_id: string;
  condition_field: string;
  operator: string;
  condition_value: string;
  action_type: string;
}

export interface Workflow {
  id: string;
  name: string;
  trigger_type: string;
  is_active: boolean;
  created_at: string;
  rules: WorkflowRule[];
}

export interface SLA {
  id: string;
  lead_id: string;
  response_due_at: string;
  resolution_due_at: string;
  is_response_breached: boolean;
  is_resolution_breached: boolean;
}
