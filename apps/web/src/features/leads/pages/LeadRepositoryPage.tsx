import React, { useState } from 'react';
import { LeadDetailView } from '../components/LeadDetailView';
import { LeadMergeModal } from '../components/LeadMergeModal';
import { LeadTable } from '../components/LeadTable';
import { useLeadDetail } from '../hooks/useLeadDetail';
import { useLeads } from '../hooks/useLeads';
import { leadsApi } from '../services/leadsApi';

export const LeadRepositoryPage: React.FC = () => {
  const { leads, search, setSearch, status, setStatus, loading, refetchLeads } = useLeads();
  const [selectedLeadId, setSelectedLeadId] = useState<string | null>(null);
  const { lead: selectedLead, refetchLead } = useLeadDetail(selectedLeadId);

  const [isMergeModalOpen, setIsMergeModalOpen] = useState<boolean>(false);

  const handleUpdateStatus = async (newStatus: string) => {
    if (!selectedLeadId) return;
    try {
      await leadsApi.updateLead(selectedLeadId, { status: newStatus });
      await refetchLead();
      await refetchLeads();
    } catch (e) {
      console.error('Failed to update lead status', e);
    }
  };

  const handleArchiveLead = async (leadId: string) => {
    try {
      await leadsApi.archiveLead(leadId);
      if (selectedLeadId === leadId) setSelectedLeadId(null);
      await refetchLeads();
    } catch (e) {
      console.error('Failed to archive lead', e);
    }
  };

  const handleFavoriteLead = async (leadId: string) => {
    const target = leads.find((l) => l.id === leadId);
    if (!target) return;
    try {
      await leadsApi.updateLead(leadId, { is_favorite: !target.is_favorite });
      await refetchLeads();
    } catch (e) {
      console.error('Failed to favorite lead', e);
    }
  };

  const handleConfirmMerge = async (secondaryLeadIds: string[]) => {
    if (!selectedLeadId) return;
    try {
      await leadsApi.mergeLeads(selectedLeadId, secondaryLeadIds);
      setIsMergeModalOpen(false);
      await refetchLead();
      await refetchLeads();
    } catch (e) {
      console.error('Failed to merge leads', e);
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
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Enterprise Lead Repository</h1>
        <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
          Master Source of Truth for Extracted Lead, Contact, Company Records & Audit Timelines.
        </p>
      </div>

      {/* Controls */}
      <div style={{ display: 'flex', gap: '16px', marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Search by Lead, Contact Name, Company, GST..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            flex: 1,
            background: '#1a1d24',
            color: '#fff',
            border: '1px solid #374151',
            borderRadius: '6px',
            padding: '10px 16px',
          }}
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          style={{
            background: '#1a1d24',
            color: '#fff',
            border: '1px solid #374151',
            borderRadius: '6px',
            padding: '10px 16px',
          }}
        >
          <option value="">All Statuses</option>
          <option value="New">New</option>
          <option value="Contacted">Contacted</option>
          <option value="Qualified">Qualified</option>
          <option value="Interested">Interested</option>
          <option value="Proposal">Proposal</option>
          <option value="Won">Won</option>
          <option value="Lost">Lost</option>
        </select>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: selectedLead ? '1fr 1fr' : '1fr', gap: '20px' }}>
        <LeadTable
          leads={leads}
          selectedLeadId={selectedLeadId}
          onSelectLead={setSelectedLeadId}
          onArchiveLead={handleArchiveLead}
          onFavoriteLead={handleFavoriteLead}
          loading={loading}
        />

        {selectedLead && (
          <LeadDetailView
            lead={selectedLead}
            onUpdateStatus={handleUpdateStatus}
            onMergeClick={() => setIsMergeModalOpen(true)}
          />
        )}
      </div>

      {selectedLead && (
        <LeadMergeModal
          primaryLead={selectedLead}
          allLeads={leads}
          isOpen={isMergeModalOpen}
          onClose={() => setIsMergeModalOpen(false)}
          onConfirmMerge={handleConfirmMerge}
        />
      )}
    </div>
  );
};

export default LeadRepositoryPage;
