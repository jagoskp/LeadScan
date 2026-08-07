import React from 'react';
import { DuplicateMatch } from '../types/identity';
import { ConfidenceBadge } from './ConfidenceBadge';

interface Props {
  matches: DuplicateMatch[];
  onSelectPair: (primaryId: string, secondaryId: string) => void;
  loading: boolean;
}

export const DuplicateMatchList: React.FC<Props> = ({ matches, onSelectPair, loading }) => {
  if (loading) return <p style={{ color: '#9ca3af' }}>Scanning identity resolution engine...</p>;
  if (matches.length === 0) return <p style={{ color: '#9ca3af' }}>No duplicate pairs detected.</p>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {matches.map((match) => (
        <div
          key={match.id}
          style={{
            background: '#1a1d24',
            border: '1px solid #374151',
            borderRadius: '8px',
            padding: '16px',
            color: '#fff',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
              <span style={{ fontWeight: 700, color: '#60a5fa' }}>Lead pair ({match.primary_lead_id.substring(0, 8)}... & {match.secondary_lead_id.substring(0, 8)}...)</span>
              <ConfidenceBadge level={match.confidence_level} />
            </div>
            <div style={{ fontSize: '0.85rem', color: '#9ca3af' }}>
              Match Type: <strong>{match.match_type.toUpperCase()}</strong> • Score: <strong style={{ color: '#10B981' }}>{match.duplicate_score.toFixed(1)}</strong>
            </div>
          </div>

          <button
            onClick={() => onSelectPair(match.primary_lead_id, match.secondary_lead_id)}
            style={{
              background: '#3B82F6',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              padding: '8px 16px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            ⚡ Preview & Merge
          </button>
        </div>
      ))}
    </div>
  );
};
