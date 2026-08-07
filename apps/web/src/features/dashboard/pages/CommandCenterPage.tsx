import React, { useState } from 'react';
import { CommandPalette } from '../components/CommandPalette';
import { KPICardGrid } from '../components/KPICardGrid';
import { LiveMonitorWidget } from '../components/LiveMonitorWidget';
import { SystemHealthWidget } from '../components/SystemHealthWidget';
import { useCommandCenter } from '../hooks/useCommandCenter';
import { CommandCenterTelemetry } from '../types/dashboard';

const defaultTelemetry: CommandCenterTelemetry = {
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

export const CommandCenterPage: React.FC = () => {
  const { telemetry } = useCommandCenter();
  const [isPaletteOpen, setIsPaletteOpen] = useState<boolean>(false);

  const activeTelemetry = telemetry || defaultTelemetry;

  return (
    <div
      style={{
        padding: '32px',
        background: '#0f1117',
        minHeight: '100vh',
        color: '#fff',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Enterprise Command Center</h1>
          <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
            Operational Control Center across Lead Repository, Google Sync, Universal Search, Assets, Identity, & Workflows.
          </p>
        </div>

        <button
          onClick={() => setIsPaletteOpen(true)}
          style={{
            background: '#374151',
            color: '#fff',
            border: '1px solid #4b5563',
            borderRadius: '6px',
            padding: '10px 18px',
            fontSize: '0.85rem',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          ⌨️ Command Palette <kbd style={{ background: '#111827', padding: '2px 6px', borderRadius: '4px', marginLeft: '6px' }}>Ctrl + K</kbd>
        </button>
      </div>

      <div>
        <KPICardGrid cards={activeTelemetry.kpi_cards || defaultTelemetry.kpi_cards} />
        <LiveMonitorWidget monitors={activeTelemetry.live_monitors || defaultTelemetry.live_monitors} />
        <SystemHealthWidget healthItems={activeTelemetry.system_health || defaultTelemetry.system_health} />
      </div>

      <CommandPalette isOpen={isPaletteOpen} onClose={() => setIsPaletteOpen(false)} />
    </div>
  );
};

export default CommandCenterPage;
