import React from 'react';
import { Contact } from '../types/leads';

interface Props {
  contacts: Contact[];
}

export const ContactList: React.FC<Props> = ({ contacts }) => {
  if (!contacts || contacts.length === 0) {
    return <p style={{ color: '#9ca3af', fontSize: '0.85rem' }}>No contacts found.</p>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
      {contacts.map((c) => (
        <div key={c.id} style={{ background: '#111827', border: '1px solid #374151', borderRadius: '6px', padding: '12px', color: '#fff' }}>
          <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>
            👤 {c.first_name} {c.last_name || ''} {c.designation && <span style={{ color: '#9ca3af', fontWeight: 400 }}>({c.designation})</span>}
          </div>
          <div style={{ fontSize: '0.8rem', color: '#9ca3af', marginTop: '4px' }}>
            {c.emails.length > 0 && <div>📧 {c.emails.join(', ')}</div>}
            {c.phones.length > 0 && <div>📞 {c.phones.join(', ')}</div>}
          </div>
        </div>
      ))}
    </div>
  );
};
