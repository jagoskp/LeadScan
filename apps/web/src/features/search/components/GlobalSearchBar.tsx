import React, { useState } from 'react';
import { useAutocomplete } from '../hooks/useAutocomplete';

interface Props {
  query: string;
  onSearch: (query: string) => void;
  onSaveClick: () => void;
}

export const GlobalSearchBar: React.FC<Props> = ({ query: initialQuery, onSearch, onSaveClick }) => {
  const [inputVal, setInputVal] = useState<string>(initialQuery);
  const { suggestions } = useAutocomplete(inputVal);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      setShowSuggestions(false);
      onSearch(inputVal);
    }
  };

  return (
    <div style={{ position: 'relative', width: '100%', marginBottom: '20px' }}>
      <div style={{ display: 'flex', gap: '12px' }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <input
            type="text"
            placeholder="Global search across Leads, Contacts, GST, Notes, OCR & AI..."
            value={inputVal}
            onChange={(e) => {
              setInputVal(e.target.value);
              setShowSuggestions(true);
            }}
            onKeyDown={handleKeyDown}
            style={{
              width: '100%',
              background: '#1a1d24',
              color: '#fff',
              border: '2px solid #3B82F6',
              borderRadius: '8px',
              padding: '12px 16px',
              fontSize: '1rem',
              outline: 'none',
              boxSizing: 'border-box',
            }}
          />

          {showSuggestions && suggestions.length > 0 && (
            <div
              style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                right: 0,
                background: '#1f2937',
                border: '1px solid #374151',
                borderRadius: '6px',
                marginTop: '4px',
                zIndex: 500,
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)',
              }}
            >
              {suggestions.map((sug, idx) => (
                <div
                  key={idx}
                  onClick={() => {
                    setInputVal(sug.suggestion);
                    setShowSuggestions(false);
                    onSearch(sug.suggestion);
                  }}
                  style={{
                    padding: '10px 16px',
                    color: '#fff',
                    borderBottom: '1px solid #374151',
                    cursor: 'pointer',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    fontSize: '0.9rem',
                  }}
                >
                  <div>🔍 {sug.suggestion}</div>
                  <div style={{ fontSize: '0.75rem', color: '#9ca3af', background: '#111827', padding: '2px 6px', borderRadius: '4px' }}>
                    {sug.target_field}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <button
          onClick={() => onSearch(inputVal)}
          style={{
            background: '#3B82F6',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            padding: '12px 24px',
            fontWeight: 700,
            cursor: 'pointer',
          }}
        >
          Search
        </button>

        <button
          onClick={onSaveClick}
          style={{
            background: '#374151',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            padding: '12px 16px',
            cursor: 'pointer',
          }}
        >
          🔖 Save Query
        </button>
      </div>
    </div>
  );
};
