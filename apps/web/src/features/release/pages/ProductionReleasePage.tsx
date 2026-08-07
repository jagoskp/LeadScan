import React from 'react';
import { CertificationBadge } from '../components/CertificationBadge';
import { ProductionChecklistCard } from '../components/ProductionChecklistCard';
import { useReleaseCertification } from '../hooks/useReleaseCertification';

export const ProductionReleasePage: React.FC = () => {
  const { report, checklist, loading, refetch } = useReleaseCertification();

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
          <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Production Certification (RC-1 GA)</h1>
          <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
            Final Enterprise Certification across GP-001 → GP-020 and BF-001 → BF-019.
          </p>
        </div>

        <button
          onClick={refetch}
          style={{
            background: '#10B981',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '10px 20px',
            fontSize: '0.9rem',
            fontWeight: 700,
            cursor: 'pointer',
          }}
        >
          🔄 Re-Run Full Certification Audit
        </button>
      </div>

      {loading && !report ? (
        <p style={{ color: '#9ca3af' }}>Executing Full Production Certification Audit...</p>
      ) : report ? (
        <div>
          <CertificationBadge
            version={report.release_version}
            status={report.certification_status}
            score={report.overall_score}
          />

          {checklist && <ProductionChecklistCard checklist={checklist} />}

          <div style={{ background: '#1a1d24', border: '1px solid #374151', borderRadius: '8px', padding: '20px', color: '#fff', marginTop: '24px' }}>
            <h3 style={{ margin: '0 0 16px 0', fontSize: '1.1rem' }}>🛡️ End-to-End Component Audit Results</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {report.checks.map((check, idx) => (
                <div key={idx} style={{ background: '#111827', padding: '12px 16px', borderRadius: '6px', border: '1px solid #374151' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.9rem', color: '#60a5fa' }}>{check.component}</span>
                    <span style={{ color: '#10B981', fontWeight: 800, fontSize: '0.8rem' }}>✔ {check.status}</span>
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#9ca3af' }}>{check.details}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <p style={{ color: '#ef4444' }}>Certification Audit Failed.</p>
      )}
    </div>
  );
};

export default ProductionReleasePage;
