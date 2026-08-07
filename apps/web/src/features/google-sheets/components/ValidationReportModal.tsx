import React from 'react';
import { MappingValidationReport } from '../types/googleSheets';

interface Props {
  report: MappingValidationReport | null;
  isOpen: boolean;
  onClose: () => void;
  onProceedWithRemapping: () => void;
}

export const ValidationReportModal: React.FC<Props> = ({
  report,
  isOpen,
  onClose,
  onProceedWithRemapping,
}) => {
  if (!isOpen || !report) return null;

  const isValid = report.status === 'Valid';

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
          maxWidth: '500px',
          width: '90%',
          color: '#fff',
        }}
      >
        <h3 style={{ margin: 0, fontSize: '1.2rem', marginBottom: '12px' }}>
          {isValid ? '✅ Mapping Validation Passed' : '⚠️ Mapping Validation Report'}
        </h3>

        <div style={{ fontSize: '0.9rem', marginBottom: '16px' }}>
          <div>
            <strong>Status:</strong> {report.status}
          </div>
          {report.missing_columns.length > 0 && (
            <div style={{ marginTop: '8px', color: '#f87171' }}>
              <strong>Missing Mapped Columns:</strong> {report.missing_columns.join(', ')}
            </div>
          )}
          {report.new_columns.length > 0 && (
            <div style={{ marginTop: '8px', color: '#60a5fa' }}>
              <strong>Newly Discovered Columns:</strong> {report.new_columns.join(', ')}
            </div>
          )}
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
            Close
          </button>
          {!isValid && (
            <button
              onClick={onProceedWithRemapping}
              style={{
                background: '#34A853',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                padding: '8px 16px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Open Auto Remapping Assistant
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
