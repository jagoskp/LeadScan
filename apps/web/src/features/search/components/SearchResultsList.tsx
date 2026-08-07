import React from 'react';
import { UniversalSearchResponse } from '../types/search';
import { SearchHighlightItem } from './SearchHighlightItem';

interface Props {
  response: UniversalSearchResponse | null;
  loading: boolean;
}

export const SearchResultsList: React.FC<Props> = ({ response, loading }) => {
  if (loading) return <p style={{ color: '#9ca3af' }}>Scanning platform search indices...</p>;
  if (!response) return <p style={{ color: '#9ca3af' }}>Enter a query above to initiate universal search.</p>;
  if (response.results.length === 0) {
    return <p style={{ color: '#9ca3af' }}>No matching records found for query: &quot;{response.query}&quot;</p>;
  }

  return (
    <div>
      <div style={{ color: '#9ca3af', fontSize: '0.85rem', marginBottom: '16px' }}>
        Found <strong>{response.total_matches}</strong> match(es) for &quot;{response.query}&quot;
      </div>
      {response.results.map((item) => (
        <SearchHighlightItem key={item.id} item={item} />
      ))}
    </div>
  );
};
