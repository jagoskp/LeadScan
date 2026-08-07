import { useCallback, useState } from 'react';
import { searchApi } from '../services/searchApi';
import { SearchFilterOptions, UniversalSearchResponse } from '../types/search';

export function useUniversalSearch() {
  const [response, setResponse] = useState<UniversalSearchResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [query, setQuery] = useState<string>('');
  const [filters, setFilters] = useState<SearchFilterOptions>({});

  const executeSearch = useCallback(async (q: string, filterOptions?: SearchFilterOptions) => {
    if (!q.trim()) return;
    setLoading(true);
    setQuery(q);
    try {
      const res = await searchApi.executeSearch(q, filterOptions || filters);
      setResponse(res);
    } catch (e) {
      console.error('Universal search error', e);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  return {
    query,
    setQuery,
    filters,
    setFilters,
    response,
    loading,
    executeSearch,
  };
}
