import React, { useState } from 'react';
import { GlobalSearchBar } from '../components/GlobalSearchBar';
import { RecentSearchesList } from '../components/RecentSearchesList';
import { SavedSearchModal } from '../components/SavedSearchModal';
import { SearchFilterPanel } from '../components/SearchFilterPanel';
import { SearchResultsList } from '../components/SearchResultsList';
import { useSavedSearches } from '../hooks/useSavedSearches';
import { useUniversalSearch } from '../hooks/useUniversalSearch';

export const UniversalSearchPage: React.FC = () => {
  const { query, filters, setFilters, response, loading, executeSearch } = useUniversalSearch();
  const { savedSearches, saveQuery } = useSavedSearches();
  const [isSaveModalOpen, setIsSaveModalOpen] = useState<boolean>(false);

  const handleSaveConfirm = async (title: string) => {
    await saveQuery(title, query, filters as Record<string, unknown>);
    setIsSaveModalOpen(false);
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
        <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Enterprise Universal Search Engine</h1>
        <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
          Platform-wide unified search engine indexing Leads, Contacts, Companies, GST, Notes, OCR & AI outputs.
        </p>
      </div>

      <GlobalSearchBar
        query={query}
        onSearch={(q) => executeSearch(q)}
        onSaveClick={() => setIsSaveModalOpen(true)}
      />

      <RecentSearchesList savedSearches={savedSearches} onSelectSearch={(q) => executeSearch(q)} />

      <SearchFilterPanel filters={filters} onChangeFilters={setFilters} />

      <SearchResultsList response={response} loading={loading} />

      <SavedSearchModal
        query={query}
        isOpen={isSaveModalOpen}
        onClose={() => setIsSaveModalOpen(false)}
        onConfirmSave={handleSaveConfirm}
      />
    </div>
  );
};

export default UniversalSearchPage;
