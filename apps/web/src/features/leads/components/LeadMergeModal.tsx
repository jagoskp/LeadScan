import React, { useState } from 'react';
import { Lead } from '../types/leads';

interface Props {
  primaryLead: Lead;
  allLeads: Lead[];
  isOpen: boolean;
  onClose: () => void;
  onConfirmMerge: (secondaryLeadIds: string[]) => void;
}

export const LeadMergeModal: React.FC<Props> = ({
  primaryLead,
  allLeads,
  isOpen,
  onClose,
  onConfirmMerge,
}) => {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  if (!isOpen) return null;

  const candidateLeads = allLeads.filter((l) => l.id !== primaryLead.id);

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

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
          maxWidth: '550px',
          width: '90%',
          color: '#fff',
        }}
      >
        <h3 style={{ margin: 0, fontSize: '1.2rem', marginBottom: '8px' }}>⚡ Merge Duplicate Leads</h3>
        <p style={{ color: '#9ca3af', fontSize: '0.85rem', marginBottom: '16px' }}>
          Select secondary leads to merge into primary record: <strong>{primaryLead.title}</strong>
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '250px', overflowY: 'auto', marginBottom: '20px' }}>
          {candidateLeads.map((cand) => (
            <label
              key={cand.id}
              style={{
                background: '#111827',
                border: '1px solid #374151',
                borderRadius: '6px',
                padding: '10px',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                cursor: 'pointer',
              }}
            >
              <input
                type="checkbox"
                checked={selectedIds.includes(cand.id)}
                onChange={() => toggleSelect(cand.id)}
              />
              <div>
                <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{cand.title}</div>
                <div style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{cand.company?.company_name || 'No Company'}</div>
              </div>
            </label>
          ))}
        </div>

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
            disabled={selectedIds.length === 0}
            onClick={() => onConfirmMerge(selectedIds)}
            style={{
              background: selectedIds.length === 0 ? '#4b5563' : '#3B82F6',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              padding: '8px 16px',
              fontWeight: 600,
              cursor: selectedIds.length === 0 ? 'not-allowed' : 'pointer',
            }}
          >
            Confirm Merge ({selectedIds.length})
          </button>
        </div>
      </div>
    </div>
  );
};
