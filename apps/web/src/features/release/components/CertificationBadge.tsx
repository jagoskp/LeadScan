import React from 'react';

interface Props {
  version: string;
  status: string;
  score: number;
}

export const CertificationBadge: React.FC<Props> = ({ version, status, score }) => {
  return (
    <div
      style={{
        background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
        borderRadius: '12px',
        padding: '24px',
        color: '#fff',
        boxShadow: '0 10px 15px -3px rgba(16, 185, 129, 0.3)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '24px',
      }}
    >
      <div>
        <div style={{ fontSize: '0.8rem', fontWeight: 800, letterSpacing: '1px', textTransform: 'uppercase', opacity: 0.9 }}>
          ENTERPRISE CERTIFIED RELEASE CANDIDATE
        </div>
        <div style={{ fontSize: '2rem', fontWeight: 900, marginTop: '4px' }}>
          LeadScan AI {version} ({status})
        </div>
        <p style={{ margin: '4px 0 0 0', fontSize: '0.9rem', opacity: 0.95 }}>
          Certified General Availability (GA) build ready for high-concurrency production deployment.
        </p>
      </div>

      <div style={{ background: 'rgba(255,255,255,0.2)', padding: '16px 24px', borderRadius: '8px', textAlign: 'center' }}>
        <div style={{ fontSize: '2.2rem', fontWeight: 900 }}>{score}%</div>
        <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>AUDIT SCORE</div>
      </div>
    </div>
  );
};
