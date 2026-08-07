import React, { useState } from 'react';

interface Props {
  query: string;
  isOpen: boolean;
  onClose: () => void;
  onConfirmSave: (title: string) => void;
}

export const SavedSearchModal: React.FC<Props> = ({ query, isOpen, onClose, onConfirmSave }) => {
  const [title, setTitle] = useState<string>(`Bookmark: ${query}`);

  if (!isOpen) return null;

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <div style={{ background: '#1f2937', borderRadius: '8px', padding: '24px', maxWidth: '450px', width: '90%', color: '#fff' }}>
        <h3 style={{ margin: '0 0 12px 0' }}>🔖 Save Search Query</h3>
        <p style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Query: <strong>{query}</strong></p>

        <label style={{ fontSize: '0.8rem', color: '#d1d5db', display: 'block', marginBottom: '6px' }}>Saved Search Title</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ width: '100%', background: '#111827', color: '#fff', border: '1px solid #374151', borderRadius: '4px', padding: '8px 12px', marginBottom: '20px' }}
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button onClick={onClose} style={{ background: '#374151', color: '#fff', border: 'none', borderRadius: '4px', padding: '8px 16px', cursor: 'pointer' }}>
            Cancel
          </button>
          <button
            onClick={() => onConfirmSave(title)}
            style={{ background: '#3B82F6', color: '#fff', border: 'none', borderRadius: '4px', padding: '8px 16px', fontWeight: 600, cursor: 'pointer' }}
          >
            Save Query
          </button>
        </div>
      </div>
    </div>
  );
};
