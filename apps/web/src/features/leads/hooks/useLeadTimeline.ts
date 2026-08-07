import { useCallback, useEffect, useState } from 'react';
import { leadsApi } from '../services/leadsApi';
import { LeadTimelineItem } from '../types/leads';

export function useLeadTimeline(leadId: string | null) {
  const [timeline, setTimeline] = useState<LeadTimelineItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchTimeline = useCallback(async () => {
    if (!leadId) return;
    setLoading(true);
    try {
      const list = await leadsApi.getTimeline(leadId);
      setTimeline(list);
    } catch (e) {
      console.error('Failed to load lead timeline', e);
    } finally {
      setLoading(false);
    }
  }, [leadId]);

  useEffect(() => {
    fetchTimeline();
  }, [fetchTimeline]);

  return { timeline, loading, refetchTimeline: fetchTimeline };
}
