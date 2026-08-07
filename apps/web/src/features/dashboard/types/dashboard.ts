export interface KPICard {
  title: string;
  value: string | number;
  change_pct: number;
  trend: 'up' | 'down' | 'neutral';
  icon: string;
}

export interface LiveMonitorItem {
  queue_name: string;
  active_count: number;
  pending_count: number;
  failed_count: number;
  status: string;
}

export interface SystemHealthItem {
  component: string;
  status: 'operational' | 'degraded' | 'outage';
  latency_ms: number;
  last_check_at: string;
}

export interface CommandCenterTelemetry {
  todays_scans: number;
  todays_leads: number;
  pending_reviews: number;
  pending_workflows: number;
  google_sync_status: string;
  storage_usage_mb: number;
  kpi_cards: KPICard[];
  live_monitors: LiveMonitorItem[];
  system_health: SystemHealthItem[];
}
