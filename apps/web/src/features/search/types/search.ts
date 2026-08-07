export interface SearchFilterOptions {
  date_from?: string;
  date_to?: string;
  status?: string;
  owner_id?: string;
  tags?: string[];
  company_name?: string;
  source_type?: string;
}

export interface SearchResultItem {
  id: string;
  lead_id?: string;
  document_id?: string;
  company_id?: string;
  contact_id?: string;
  title: string;
  company_name?: string;
  gst_number?: string;
  email?: string;
  phone?: string;
  matched_field: string;
  highlighted_match: string;
  score: number;
  source_type: string;
  created_at: string;
}

export interface UniversalSearchResponse {
  query: string;
  total_matches: number;
  results: SearchResultItem[];
  page: number;
  page_size: number;
}

export interface SavedSearch {
  id: string;
  user_id: string;
  title: string;
  query_string: string;
  filters?: Record<string, unknown>;
  is_pinned: boolean;
  created_at: string;
}

export interface RecentSearch {
  id: string;
  query_string: string;
  results_count: number;
  created_at: string;
}

export interface AutocompleteSuggestion {
  suggestion: string;
  target_field: string;
  score: number;
}
