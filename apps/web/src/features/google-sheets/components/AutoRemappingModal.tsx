import React from 'react';
import { RemappingSuggestion } from '../types/googleSheets';

interface Props {
  suggestions: RemappingSuggestion[];
  isOpen: boolean;
  onClose: () => void;
  onApplyRemapping: () => void;
}

export const AutoRemappingModal: React.FC<Props> = ({
  suggestions,
  isOpen,
  onClose,
  onApplyRemapping,
}) => {
  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
    >
      <div
        style={{
          background: '#1f2937',
          borderRadius: '8px',
          padding: '24px',
          maxWidth: '600px',
          width: '90%',
          color: '#fff',
        }}
      >
        <h3 style={{ margin: 0, fontSize: '1.2rem', marginBottom: '8px' }}>🤖 Auto Remapping Assistant</h3>
        <p style={{ color: '#9ca3af', fontSize: '0.85rem', marginBottom: '16px' }}>
          Detected renamed or missing columns. Intelligent suggestions derived from Levenshtein similarity & synonym dictionaries.
        </p>

        {suggestions.length === 0 ? (
          <p style={{ color: '#9ca3af' }}>No remapping suggestions required.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px' }}>
            {suggestions.map((sug) => (
              <div
                key={sug.id}
                style={{
                  background: '#111827',
                  border: '1px solid #374151',
                  borderRadius: '6px',
                  padding: '12px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>
                    <span style={{ color: '#f87171' }}>{sug.target_entity_field}</span> ➔{' '}
                    <span style={{ color: '#34A853' }}>{sug.source_column}</span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '4px' }}>
                    {sug.suggestion_reason}
                  </div>
                </div>
                <div
                  style={{
                    background: 'rgba(52, 168, 83, 0.2)',
                    color: '#34A853',
                    padding: '4px 8px',
                    borderRadius: '4px',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                  }}
                >
                  {Math.round(sug.similarity_score * 100)}% Match
                </div>
              </div>
            ))}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button
            onClick={onClose}
            style={{
              background: '#374151',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              padding: '8px 16px',
              cursor: 'pointer',
            }}
          >
            Cancel
          </button>
          <button
            onClick={onApplyRemapping}
            style={{
              background: '#4285F4',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              padding: '8px 16px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Accept & Apply Remappings
          </button>
        </div>
      </div>
    </div>
  );
};
