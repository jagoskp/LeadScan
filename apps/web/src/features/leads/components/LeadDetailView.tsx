import React, { useState } from 'react';
import { Lead } from '../types/leads';
import { CompanyCard } from './CompanyCard';
import { ContactList } from './ContactList';
import { LeadNotesTab } from './LeadNotesTab';
import { LeadStatusBadge } from './LeadStatusBadge';
import { LeadTimelineView } from './LeadTimelineView';

interface Props {
  lead: Lead;
  onUpdateStatus: (newStatus: string) => void;
  onMergeClick: () => void;
}

export const LeadDetailView: React.FC<Props> = ({ lead, onUpdateStatus, onMergeClick }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'contacts' | 'notes' | 'timeline'>('overview');

  return (
    <div style={{ background: '#1a1d24', borderRadius: '8px', padding: '20px', color: '#fff' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <h2 style={{ margin: 0, fontSize: '1.4rem', fontWeight: 700 }}>{lead.title}</h2>
            <LeadStatusBadge status={lead.status} />
          </div>
          <div style={{ color: '#9ca3af', fontSize: '0.85rem', marginTop: '4px' }}>
            ID: {lead.id} • Created: {new Date(lead.created_at).toLocaleDateString()}
          </div>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <select
            value={lead.status}
            onChange={(e) => onUpdateStatus(e.target.value)}
            style={{ background: '#111827', color: '#fff', border: '1px solid #374151', borderRadius: '4px', padding: '6px 12px' }}
          >
            <option value="New">New</option>
            <option value="Contacted">Contacted</option>
            <option value="Qualified">Qualified</option>
            <option value="Interested">Interested</option>
            <option value="Proposal">Proposal</option>
            <option value="Won">Won</option>
            <option value="Lost">Lost</option>
          </select>
          <button
            onClick={onMergeClick}
            style={{ background: '#374151', color: '#fff', border: 'none', borderRadius: '4px', padding: '6px 12px', cursor: 'pointer' }}
          >
            ⚡ Merge
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid #374151', marginBottom: '16px' }}>
        {(['overview', 'contacts', 'notes', 'timeline'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              background: 'none',
              border: 'none',
              borderBottom: activeTab === tab ? '2px solid #3B82F6' : '2px solid transparent',
              color: activeTab === tab ? '#60a5fa' : '#9ca3af',
              padding: '8px 16px',
              fontWeight: 600,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div>
            <h4 style={{ margin: '0 0 8px 0', fontSize: '0.95rem' }}>Company Details</h4>
            <CompanyCard company={lead.company} />
          </div>
          <div>
            <h4 style={{ margin: '0 0 8px 0', fontSize: '0.95rem' }}>Primary Contact</h4>
            <ContactList contacts={lead.contacts.filter((c) => c.is_primary)} />
          </div>
        </div>
      )}

      {activeTab === 'contacts' && <ContactList contacts={lead.contacts} />}

      {activeTab === 'notes' && <LeadNotesTab notes={lead.notes} />}

      {activeTab === 'timeline' && <LeadTimelineView leadId={lead.id} />}
    </div>
  );
};
