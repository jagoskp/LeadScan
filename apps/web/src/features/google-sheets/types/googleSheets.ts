export interface GoogleAccount {
  id: string;
  account_email: string;
  account_label?: string;
  is_default: boolean;
  is_active: boolean;
  created_at: string;
}

export interface Spreadsheet {
  id: string;
  title: string;
  is_favorite: boolean;
}

export interface Worksheet {
  worksheet_id: string;
  title: string;
  index: number;
  row_count: number;
  column_count: number;
}

export interface SpreadsheetColumn {
  id: string;
  worksheet_id: string;
  name: string;
  index: number;
  data_type: string;
  is_hidden: boolean;
  is_custom: boolean;
}

export interface ColumnDiscoveryResponse {
  spreadsheet_id: string;
  worksheet_title: string;
  discovered_headers: string[];
  column_details: SpreadsheetColumn[];
  is_cache_hit: boolean;
}

export interface RemappingSuggestion {
  id: string;
  source_column: string;
  target_entity_field: string;
  similarity_score: number;
  suggestion_reason: string;
  status: 'Pending' | 'Accepted' | 'Rejected';
}

export interface MappingValidationReport {
  id: string;
  sheet_id: string;
  worksheet_id: string;
  status: 'Valid' | 'MissingColumns' | 'RenamedColumns' | 'Invalid';
  missing_columns: string[];
  new_columns: string[];
  suggestions: RemappingSuggestion[];
  report_data: Record<string, unknown>;
  created_at: string;
}

export interface SyncJob {
  id: string;
  profile_id?: string;
  spreadsheet_id: string;
  worksheet_id: string;
  sync_mode: string;
  status: string;
  total_rows: number;
  processed_rows: number;
  success_rows: number;
  failed_rows: number;
  retry_count: number;
  max_retries: number;
  created_at: string;
}

export interface SyncHistoryItem {
  id: string;
  job_id: string;
  spreadsheet_id: string;
  worksheet_id: string;
  rows_processed: number;
  duration_ms: number;
  retries: number;
  status: string;
  error_message?: string;
  validation_result?: MappingValidationReport;
  created_at: string;
}
