import {
  AutocompleteSuggestion,
  RecentSearch,
  SavedSearch,
  SearchFilterOptions,
  UniversalSearchResponse,
} from '../types/search';

const BASE_URL = '/api/v1/search';

export const searchApi = {
  async executeSearch(
    query: string,
    filters?: SearchFilterOptions,
    sortBy: string = 'relevance',
    page: number = 1
  ): Promise<UniversalSearchResponse> {
    const res = await fetch(`${BASE_URL}/universal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, filters, sort_by: sortBy, page, page_size: 20 }),
    });
    if (!res.ok) throw new Error('Search execution failed');
    return res.json();
  },

  async getAutocomplete(prefix: string): Promise<AutocompleteSuggestion[]> {
    const res = await fetch(`${BASE_URL}/suggestions?prefix=${encodeURIComponent(prefix)}`);
    if (!res.ok) throw new Error('Failed to fetch suggestions');
    return res.json();
  },

  async saveSearch(title: string, query: string, filters?: Record<string, unknown>): Promise<SavedSearch> {
    const res = await fetch(`${BASE_URL}/saved-searches`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, query_string: query, filters }),
    });
    if (!res.ok) throw new Error('Failed to save search');
    return res.json();
  },

  async getSavedSearches(): Promise<SavedSearch[]> {
    const res = await fetch(`${BASE_URL}/saved-searches`);
    if (!res.ok) throw new Error('Failed to fetch saved searches');
    return res.json();
  },

  async getRecentSearches(): Promise<RecentSearch[]> {
    const res = await fetch(`${BASE_URL}/recent`);
    if (!res.ok) throw new Error('Failed to fetch recent searches');
    return res.json();
  },
};
