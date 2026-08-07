export interface Contact {
  id: string;
  lead_id: string;
  first_name: string;
  last_name?: string;
  designation?: string;
  is_primary: boolean;
  phones: string[];
  emails: string[];
  websites: string[];
  addresses: string[];
  social_profiles: string[];
  custom_fields: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface Company {
  id: string;
  company_name: string;
  logo_url?: string;
  industry?: string;
  gst_number?: string;
  website?: string;
  address?: string;
  departments?: string[];
  employees_count?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface LeadTag {
  id: string;
  tag_name: string;
  color: string;
  is_system: boolean;
}

export interface LeadNote {
  id: string;
  content: string;
  is_pinned: boolean;
  is_internal: boolean;
  author_id?: string;
  created_at: string;
}

export interface LeadMetadata {
  id: string;
  original_image_url?: string;
  ocr_raw_output?: Record<string, unknown>;
  ai_understanding_output?: Record<string, unknown>;
  dom_entity_snapshot?: Record<string, unknown>;
  review_session_id?: string;
  google_sync_job_id?: string;
}

export interface Lead {
  id: string;
  organization_id?: string;
  company_id?: string;
  owner_id?: string;
  title: string;
  status: string;
  priority: string;
  source: string;
  lead_score: number;
  is_favorite: boolean;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
  company?: Company;
  contacts: Contact[];
  tags: LeadTag[];
  notes: LeadNote[];
  lead_metadata?: LeadMetadata;
}

export interface LeadTimelineItem {
  id: string;
  lead_id: string;
  event_type: string;
  title: string;
  description?: string;
  actor_id?: string;
  metadata_snapshot?: Record<string, unknown>;
  created_at: string;
}
