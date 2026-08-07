import React, { useState } from "react";
import { useStudioState } from "../hooks/useStudioState";
import { MappingCanvas } from "../components/MappingCanvas";
import { RuleBuilder } from "../components/RuleBuilder";
import { PreviewPanel } from "../components/PreviewPanel";
import { getLivePreview } from "../services/api";

export const MappingStudioPage: React.FC = () => {
  const { state, addRule, removeRule, selectRule, setSearch } = useStudioState(null);
  const [preview, setPreview] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleCreateRule = () => {
    addRule({
      id: Math.random().toString(),
      sourceEntityType: "Company",
      targetFieldName: "organization_name",
      fieldType: "Text",
      isRequired: true,
    });
  };

  const handleTriggerPreview = async () => {
    if (!state.profileId || !state.documentId) return;
    setLoading(true);
    try {
      const data = await getLivePreview(state.documentId, state.profileId);
      setPreview(data);
    } catch {
      // Handle error placeholder
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 p-8 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Mapping Studio</h1>
          <p className="text-slate-400 text-sm">Create, test, and manage profile configurations.</p>
        </div>
        <button
          onClick={handleCreateRule}
          className="bg-violet-600 hover:bg-violet-700 text-white font-bold px-4 py-2 rounded-lg transition"
        >
          Add Mock Rule
        </button>
      </div>

      <div className="flex gap-6">
        <MappingCanvas
          rules={state.rules}
          onRemoveRule={removeRule}
          onSelectRule={selectRule}
        />
        <RuleBuilder
          selectedRuleId={state.selectedRuleId}
          onSaveRuleConditions={() => {}}
        />
      </div>

      <PreviewPanel previewData={preview} loading={loading} />
    </div>
  );
};
export default MappingStudioPage;
