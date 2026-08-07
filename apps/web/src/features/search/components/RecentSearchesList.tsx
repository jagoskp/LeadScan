import React from 'react';
import { SavedSearch } from '../types/search';

interface Props {
  savedSearches: SavedSearch[];
  onSelectSearch: (query: string) => void;
}

export const RecentSearchesList: React.FC<Props> = ({ savedSearches, onSelectSearch }) => {
  if (!savedSearches || savedSearches.length === 0) return null;

  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '20px' }}>
      <h4 style={{ margin: '0 0 12px 0', fontSize: '0.95rem', color: '#60a5fa' }}>📌 Saved Search Presets</h4>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {savedSearches.map((s) => (
          <button
            key={s.id}
            onClick={() => onSelectSearch(s.query_string)}
            style={{
              background: '#111827',
              color: '#d1d5db',
              border: '1px solid #374151',
              borderRadius: '20px',
              padding: '6px 14px',
              fontSize: '0.8rem',
              cursor: 'pointer',
            }}
          >
            🔖 {s.title}
          </button>
        ))}
      </div>
    </div>
  );
};
