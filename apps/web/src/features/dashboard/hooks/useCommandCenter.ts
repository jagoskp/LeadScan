import { useCallback, useEffect, useState } from 'react';
import { dashboardApi } from '../services/dashboardApi';
import { CommandCenterTelemetry } from '../types/dashboard';

const initialTelemetry: CommandCenterTelemetry = {
  todays_scans: 142,
  todays_leads: 128,
  pending_reviews: 14,
  pending_workflows: 6,
  google_sync_status: 'Healthy',
  storage_usage_mb: 256.4,
  kpi_cards: [
    { title: "Today's Scans", value: 142, change_pct: 12.5, trend: 'up', icon: '📷' },
    { title: 'Verified Leads', value: 128, change_pct: 8.2, trend: 'up', icon: '📇' },
    { title: 'Pending Review', value: 14, change_pct: -4.1, trend: 'down', icon: '⚖️' },
    { title: 'Sync Status', value: 'Active', change_pct: 100, trend: 'neutral', icon: '📊' },
  ],
  live_monitors: [
    { queue_name: 'OCR Processing Queue', active_count: 3, pending_count: 12, failed_count: 0, status: 'Processing' },
    { queue_name: 'Google Sheets Batch Sync', active_count: 1, pending_count: 2, failed_count: 0, status: 'Idle' },
    { queue_name: 'AI Intelligence Extraction', active_count: 2, pending_count: 5, failed_count: 0, status: 'Processing' },
  ],
  system_health: [
    { component: 'FastAPI API Gateway', status: 'operational', latency_ms: 18, last_check_at: new Date().toISOString() },
    { component: 'OCR Engine Pipeline', status: 'operational', latency_ms: 45, last_check_at: new Date().toISOString() },
    { component: 'Google Sheets Connector', status: 'operational', latency_ms: 62, last_check_at: new Date().toISOString() },
    { component: 'PostgreSQL Database', status: 'operational', latency_ms: 12, last_check_at: new Date().toISOString() },
  ],
};

export function useCommandCenter() {
  const [telemetry, setTelemetry] = useState<CommandCenterTelemetry>(initialTelemetry);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchTelemetry = useCallback(async () => {
    setLoading(true);
    try {
      const data = await dashboardApi.getTelemetry();
      if (data) {
        setTelemetry(data);
      }
    } catch (e) {
      console.error('Failed to load telemetry', e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 30000); // 30s auto-refresh
    return () => clearInterval(interval);
  }, [fetchTelemetry]);

  return { telemetry, loading, refetchTelemetry: fetchTelemetry };
}
