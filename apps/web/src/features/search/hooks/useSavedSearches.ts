import { useCallback, useEffect, useState } from 'react';
import { searchApi } from '../services/searchApi';
import { SavedSearch } from '../types/search';

export function useSavedSearches() {
  const [savedSearches, setSavedSearches] = useState<SavedSearch[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchSavedSearches = useCallback(async () => {
    setLoading(true);
    try {
      const list = await searchApi.getSavedSearches();
      setSavedSearches(list);
    } catch (e) {
      console.error('Failed to load saved searches', e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSavedSearches();
  }, [fetchSavedSearches]);

  const saveQuery = async (title: string, query: string, filters?: Record<string, unknown>) => {
    try {
      await searchApi.saveSearch(title, query, filters);
      await fetchSavedSearches();
    } catch (e) {
      console.error('Failed to save search', e);
    }
  };

  return { savedSearches, loading, saveQuery, refetchSavedSearches: fetchSavedSearches };
}
