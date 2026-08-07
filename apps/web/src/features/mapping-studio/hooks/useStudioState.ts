import { useState } from "react";
import { MappingRule, StudioState } from "../types/studio";

export function useStudioState(initialProfileId: string | null) {
  const [state, setState] = useState<StudioState>({
    profileId: initialProfileId,
    documentId: null,
    rules: [],
    selectedRuleId: null,
    isDragging: false,
    searchQuery: "",
  });

  const addRule = (rule: MappingRule) => {
    setState((prev) => ({ ...prev, rules: [...prev.rules, rule] }));
  };

  const removeRule = (ruleId: string) => {
    setState((prev) => ({
      ...prev,
      rules: prev.rules.filter((r) => r.id !== ruleId),
    }));
  };

  const selectRule = (ruleId: string | null) => {
    setState((prev) => ({ ...prev, selectedRuleId: ruleId }));
  };

  const setSearch = (query: string) => {
    setState((prev) => ({ ...prev, searchQuery: query }));
  };

  return {
    state,
    addRule,
    removeRule,
    selectRule,
    setSearch,
  };
}
