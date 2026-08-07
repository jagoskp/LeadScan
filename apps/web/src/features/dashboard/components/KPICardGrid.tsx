import React from 'react';
import { KPICard } from '../types/dashboard';

interface Props {
  cards: KPICard[];
}

export const KPICardGrid: React.FC<Props> = ({ cards }) => {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '16px', marginBottom: '24px' }}>
      {cards.map((card, idx) => (
        <div
          key={idx}
          style={{
            background: '#1a1d24',
            border: '1px solid #374151',
            borderRadius: '8px',
            padding: '20px',
            color: '#fff',
          }}
        >
          <div style={{ fontSize: '0.8rem', color: '#9ca3af', fontWeight: 600, marginBottom: '6px' }}>{card.title}</div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#60a5fa' }}>{card.value}</div>
          <div style={{ fontSize: '0.75rem', marginTop: '6px', color: card.trend === 'up' ? '#10B981' : card.trend === 'down' ? '#EF4444' : '#9ca3af' }}>
            {card.trend === 'up' ? '▲' : card.trend === 'down' ? '▼' : '•'} {card.change_pct}% from yesterday
          </div>
        </div>
      ))}
    </div>
  );
};
