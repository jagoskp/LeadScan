import React, { useState } from 'react';
import { useMergePreview } from '../hooks/useMergePreview';
import { ConflictResolutionTable } from './ConflictResolutionTable';

interface Props {
  primaryId: string | null;
  secondaryId: string | null;
  isOpen: boolean;
  onClose: () => void;
  onConfirmMerge: (policy: string) => void;
}

export const MergePreviewModal: React.FC<Props> = ({
  primaryId,
  secondaryId,
  isOpen,
  onClose,
  onConfirmMerge,
}) => {
  const { preview, loading } = useMergePreview(primaryId, secondaryId);
  const [policy, setPolicy] = useState<string>('keep_original');

  if (!isOpen || !primaryId || !secondaryId) return null;

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
          maxWidth: '650px',
          width: '90%',
          color: '#fff',
        }}
      >
        <h3 style={{ margin: '0 0 12px 0' }}>⚡ Identity Resolution Merge Preview</h3>
        {loading ? (
          <p style={{ color: '#9ca3af' }}>Calculating field differences...</p>
        ) : preview ? (
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
              <div style={{ background: '#111827', padding: '12px', borderRadius: '6px' }}>
                <span style={{ fontSize: '0.75rem', color: '#10B981', fontWeight: 700 }}>PRIMARY RECORD</span>
                <div style={{ fontWeight: 600, fontSize: '0.95rem', marginTop: '4px' }}>{preview.primary_title}</div>
                <div style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{preview.primary_lead_id}</div>
              </div>
              <div style={{ background: '#111827', padding: '12px', borderRadius: '6px' }}>
                <span style={{ fontSize: '0.75rem', color: '#EF4444', fontWeight: 700 }}>SECONDARY RECORD (ARCHIVED)</span>
                <div style={{ fontWeight: 600, fontSize: '0.95rem', marginTop: '4px' }}>{preview.secondary_title}</div>
                <div style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{preview.secondary_lead_id}</div>
              </div>
            </div>

            <ConflictResolutionTable conflicts={preview.conflicts} />

            <div style={{ marginTop: '16px' }}>
              <label style={{ fontSize: '0.8rem', color: '#9ca3af', display: 'block', marginBottom: '6px' }}>Conflict Policy</label>
              <select
                value={policy}
                onChange={(e) => setPolicy(e.target.value)}
                style={{ width: '100%', background: '#111827', color: '#fff', border: '1px solid #374151', borderRadius: '4px', padding: '8px' }}
              >
                <option value="keep_original">Keep Primary Original Values</option>
                <option value="keep_latest">Keep Secondary Latest Values</option>
                <option value="manual">Manual Override</option>
              </select>
            </div>
          </div>
        ) : (
          <p style={{ color: '#ef4444' }}>Failed to generate preview.</p>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '20px' }}>
          <button onClick={onClose} style={{ background: '#374151', color: '#fff', border: 'none', borderRadius: '4px', padding: '8px 16px', cursor: 'pointer' }}>
            Cancel
          </button>
          <button
            onClick={() => onConfirmMerge(policy)}
            style={{ background: '#3B82F6', color: '#fff', border: 'none', borderRadius: '4px', padding: '8px 16px', fontWeight: 600, cursor: 'pointer' }}
          >
            Confirm Safe Merge
          </button>
        </div>
      </div>
    </div>
  );
};
