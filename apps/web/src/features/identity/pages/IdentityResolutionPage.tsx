import React, { useState } from 'react';
import { DuplicateMatchList } from '../components/DuplicateMatchList';
import { MergePreviewModal } from '../components/MergePreviewModal';
import { useDuplicateMatches } from '../hooks/useDuplicateMatches';
import { identityApi } from '../services/identityApi';

export const IdentityResolutionPage: React.FC = () => {
  const { matches, loading, triggerScan, refetchMatches } = useDuplicateMatches();
  const [selectedPrimary, setSelectedPrimary] = useState<string | null>(null);
  const [selectedSecondary, setSelectedSecondary] = useState<string | null>(null);
  const [isPreviewOpen, setIsPreviewOpen] = useState<boolean>(false);

  const handleSelectPair = (primaryId: string, secondaryId: string) => {
    setSelectedPrimary(primaryId);
    setSelectedSecondary(secondaryId);
    setIsPreviewOpen(true);
  };

  const handleConfirmMerge = async (policy: string) => {
    if (!selectedPrimary || !selectedSecondary) return;
    try {
      await identityApi.executeMerge(selectedPrimary, [selectedSecondary], policy);
      setIsPreviewOpen(false);
      await refetchMatches();
    } catch (e) {
      console.error('Merge execution error', e);
    }
  };

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
          <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Enterprise Identity Resolution Engine</h1>
          <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
            Multi-rule duplicate detection, confidence classification, field conflict resolution, and safe merge rollback.
          </p>
        </div>

        <button
          onClick={triggerScan}
          style={{
            background: '#3B82F6',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '10px 20px',
            fontWeight: 700,
            cursor: 'pointer',
          }}
        >
          🔍 Scan For Duplicates
        </button>
      </div>

      <DuplicateMatchList matches={matches} onSelectPair={handleSelectPair} loading={loading} />

      <MergePreviewModal
        primaryId={selectedPrimary}
        secondaryId={selectedSecondary}
        isOpen={isPreviewOpen}
        onClose={() => setIsPreviewOpen(false)}
        onConfirmMerge={handleConfirmMerge}
      />
    </div>
  );
};

export default IdentityResolutionPage;
