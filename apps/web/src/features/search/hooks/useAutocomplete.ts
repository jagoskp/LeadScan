import { useEffect, useState } from 'react';
import { searchApi } from '../services/searchApi';
import { AutocompleteSuggestion } from '../types/search';

export function useAutocomplete(prefix: string) {
  const [suggestions, setSuggestions] = useState<AutocompleteSuggestion[]>([]);

  useEffect(() => {
    if (!prefix.trim() || prefix.length < 2) {
      setSuggestions([]);
      return;
    }
    const timer = setTimeout(async () => {
      try {
        const list = await searchApi.getAutocomplete(prefix);
        setSuggestions(list);
      } catch (e) {
        console.error('Autocomplete error', e);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [prefix]);

  return { suggestions };
}
