import React, { useEffect, useState } from 'react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const CommandPalette: React.FC<Props> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState<string>('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const actions = [
    { label: '🔍 Universal Search Across All Records', category: 'Search' },
    { label: '📊 View Executive Operations Dashboard', category: 'Navigation' },
    { label: '📊 View Google Sheets Sync Connector', category: 'Connector' },
    { label: '⚡ Trigger Duplicate Identity Scan', category: 'Identity' },
    { label: '🖼️ Open Digital Asset Vault Manager', category: 'Assets' },
  ];

  const filtered = actions.filter((a) => a.label.toLowerCase().includes(query.toLowerCase()));

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.75)',
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'center',
        paddingTop: '100px',
        zIndex: 2000,
      }}
    >
      <div
        style={{
          background: '#1f2937',
          borderRadius: '12px',
          width: '90%',
          maxWidth: '600px',
          overflow: 'hidden',
          border: '1px solid #374151',
          boxShadow: '0 20px 25px -5px rgba(0,0,0,0.5)',
        }}
      >
        <div style={{ padding: '16px', borderBottom: '1px solid #374151', display: 'flex', alignItems: 'center' }}>
          <input
            type="text"
            placeholder="Type a command or search (Press Esc to close)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            style={{
              width: '100%',
              background: 'transparent',
              border: 'none',
              color: '#fff',
              fontSize: '1rem',
              outline: 'none',
            }}
          />
        </div>

        <div style={{ maxHeight: '300px', overflowY: 'auto', padding: '8px' }}>
          {filtered.map((action, idx) => (
            <div
              key={idx}
              onClick={() => {
                alert(`Executed action: ${action.label}`);
                onClose();
              }}
              style={{
                padding: '12px 16px',
                borderRadius: '6px',
                color: '#fff',
                cursor: 'pointer',
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '0.9rem',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = '#374151')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
            >
              <span>{action.label}</span>
              <span style={{ color: '#9ca3af', fontSize: '0.75rem' }}>{action.category}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
