import React from 'react';
import { GoogleAccount } from '../types/googleSheets';

interface Props {
  accounts: GoogleAccount[];
  selectedAccountId: string | null;
  onSelectAccount: (accountId: string) => void;
  onConnectAccount: () => void;
  onDisconnectAccount: (accountId: string) => void;
}

export const GoogleAccountSelector: React.FC<Props> = ({
  accounts,
  selectedAccountId,
  onSelectAccount,
  onConnectAccount,
  onDisconnectAccount,
}) => {
  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '16px', color: '#fff', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600 }}>Google Account Connection</h3>
        <button
          onClick={onConnectAccount}
          style={{
            background: 'linear-gradient(135deg, #4285F4 0%, #34A853 100%)',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 16px',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          + Connect Google Account
        </button>
      </div>

      {accounts.length === 0 ? (
        <p style={{ color: '#9ca3af', fontSize: '0.9rem' }}>No Google accounts connected. Connect an account to start syncing.</p>
      ) : (
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          {accounts.map((acc) => {
            const isSelected = acc.id === selectedAccountId;
            return (
              <div
                key={acc.id}
                onClick={() => onSelectAccount(acc.id)}
                style={{
                  border: isSelected ? '2px solid #4285F4' : '1px solid #374151',
                  background: isSelected ? 'rgba(66, 133, 244, 0.1)' : '#111827',
                  borderRadius: '6px',
                  padding: '12px',
                  minWidth: '220px',
                  cursor: 'pointer',
                  display: 'flex',
                  justify: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{acc.account_email}</div>
                  <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '4px' }}>
                    {acc.is_default ? 'Default Account' : 'Connected'}
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDisconnectAccount(acc.id);
                  }}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: '#ef4444',
                    cursor: 'pointer',
                    fontSize: '0.8rem',
                  }}
                >
                  Disconnect
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
