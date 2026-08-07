export interface DuplicateMatch {
  id: string;
  primary_lead_id: string;
  secondary_lead_id: string;
  duplicate_score: number;
  confidence_score: number;
  match_type: string;
  confidence_level: string;
  status: string;
  created_at: string;
}

export interface MergeConflict {
  id: string;
  field_name: string;
  primary_value?: string;
  secondary_value?: string;
  resolved_value?: string;
  resolution_policy: string;
}

export interface MergePreviewResponse {
  primary_lead_id: string;
  secondary_lead_id: string;
  primary_title: string;
  secondary_title: string;
  conflicts: MergeConflict[];
  has_conflicts: boolean;
  duplicate_score: number;
  confidence_level: string;
}

export interface MergeHistory {
  id: string;
  primary_lead_id: string;
  secondary_lead_id: string;
  actor_id?: string;
  merge_reason?: string;
  duplicate_score: number;
  merged_at: string;
  conflicts: MergeConflict[];
}

export interface RollbackHistory {
  id: string;
  merge_history_id: string;
  is_restored: boolean;
  restored_at?: string;
}
