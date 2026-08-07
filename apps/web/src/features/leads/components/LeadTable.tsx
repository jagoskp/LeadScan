import React from 'react';
import { Lead } from '../types/leads';
import { LeadStatusBadge } from './LeadStatusBadge';

interface Props {
  leads: Lead[];
  selectedLeadId: string | null;
  onSelectLead: (leadId: string) => void;
  onArchiveLead: (leadId: string) => void;
  onFavoriteLead: (leadId: string) => void;
  loading: boolean;
}

export const LeadTable: React.FC<Props> = ({
  leads,
  selectedLeadId,
  onSelectLead,
  onArchiveLead,
  onFavoriteLead,
  loading,
}) => {
  if (loading) return <p style={{ color: '#9ca3af' }}>Loading Master Lead Repository...</p>;
  if (leads.length === 0) return <p style={{ color: '#9ca3af' }}>No lead records found.</p>;

  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', overflow: 'hidden' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', color: '#fff', fontSize: '0.85rem' }}>
        <thead>
          <tr style={{ background: '#111827', color: '#9ca3af', textAlign: 'left', borderBottom: '1px solid #374151' }}>
            <th style={{ padding: '12px' }}>★</th>
            <th style={{ padding: '12px' }}>Lead Title / Contact</th>
            <th style={{ padding: '12px' }}>Company / GST</th>
            <th style={{ padding: '12px' }}>Status</th>
            <th style={{ padding: '12px' }}>Score</th>
            <th style={{ padding: '12px' }}>Source</th>
            <th style={{ padding: '12px', textAlign: 'right' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => {
            const isSelected = lead.id === selectedLeadId;
            const primaryContact = lead.contacts.find((c) => c.is_primary) || lead.contacts[0];
            return (
              <tr
                key={lead.id}
                onClick={() => onSelectLead(lead.id)}
                style={{
                  borderBottom: '1px solid #1f2937',
                  background: isSelected ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
                  cursor: 'pointer',
                }}
              >
                <td style={{ padding: '12px' }}>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onFavoriteLead(lead.id);
                    }}
                    style={{ background: 'none', border: 'none', color: lead.is_favorite ? '#F59E0B' : '#4b5563', cursor: 'pointer' }}
                  >
                    ★
                  </button>
                </td>
                <td style={{ padding: '12px' }}>
                  <div style={{ fontWeight: 600, color: '#60a5fa' }}>{lead.title}</div>
                  <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>
                    {primaryContact ? `${primaryContact.first_name} (${primaryContact.emails[0] || 'No Email'})` : 'No Contact'}
                  </div>
                </td>
                <td style={{ padding: '12px' }}>
                  <div>{lead.company?.company_name || 'N/A'}</div>
                  <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>
                    GST: {lead.company?.gst_number || 'None'}
                  </div>
                </td>
                <td style={{ padding: '12px' }}>
                  <LeadStatusBadge status={lead.status} />
                </td>
                <td style={{ padding: '12px', fontWeight: 600, color: '#10B981' }}>
                  {lead.lead_score.toFixed(1)}
                </td>
                <td style={{ padding: '12px', color: '#9ca3af' }}>{lead.source}</td>
                <td style={{ padding: '12px', textAlign: 'right' }}>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onArchiveLead(lead.id);
                    }}
                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '0.8rem' }}
                  >
                    Archive
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
