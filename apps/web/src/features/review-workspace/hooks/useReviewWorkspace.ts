import { useState } from "react";
import { ReviewItem, ReviewSession } from "../types/review";

export function useReviewWorkspace(initialSession: ReviewSession | null) {
  const [session, setSession] = useState<ReviewSession | null>(initialSession);
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null);
  const [confidenceFilter, setConfidenceFilter] = useState<string | null>(null);

  const updateItemValue = (itemId: string, newValue: string) => {
    if (!session) return;
    setSession({
      ...session,
      items: session.items.map((item) =>
        item.id === itemId
          ? {
              ...item,
              currentValue: newValue,
              status: "Approved",
            }
          : item
      ),
    });
  };

  const getFilteredItems = (): ReviewItem[] => {
    if (!session) return [];
    if (!confidenceFilter) return session.items;
    return session.items.filter(
      (item) => item.confidenceLevel === confidenceFilter
    );
  };

  return {
    session,
    selectedItemId,
    setSelectedItemId,
    confidenceFilter,
    setConfidenceFilter,
    updateItemValue,
    filteredItems: getFilteredItems(),
  };
}
