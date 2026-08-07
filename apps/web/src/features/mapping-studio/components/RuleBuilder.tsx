import React, { useState } from "react";

interface RuleBuilderProps {
  selectedRuleId: string | null;
  onSaveRuleConditions: (conditions: any) => void;
}

export const RuleBuilder: React.FC<RuleBuilderProps> = ({
  selectedRuleId,
  onSaveRuleConditions,
}) => {
  const [operator, setOperator] = useState("AND");

  if (!selectedRuleId) {
    return (
      <div className="w-80 p-6 bg-slate-900 border border-slate-800 rounded-xl">
        <h3 className="text-lg font-bold text-white mb-2">Rule Builder</h3>
        <p className="text-slate-500 text-sm">Select a mapping rule to build conditions.</p>
      </div>
    );
  }

  return (
    <div className="w-80 p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
      <h3 className="text-lg font-bold text-white">Rule Builder</h3>
      <div>
        <label className="text-xs font-semibold text-slate-400 block mb-1">Operator</label>
        <select
          value={operator}
          onChange={(e) => setOperator(e.target.value)}
          className="w-full bg-slate-800 border border-slate-700 text-white rounded p-2 text-sm focus:outline-none focus:border-violet-500"
        >
          <option value="AND">AND</option>
          <option value="OR">OR</option>
          <option value="NOT">NOT</option>
          <option value="IF">IF</option>
        </select>
      </div>
      <button
        onClick={() => onSaveRuleConditions({ logical_operator: operator })}
        className="w-full bg-violet-600 hover:bg-violet-700 text-white font-semibold rounded p-2 text-sm transition"
      >
        Save Rule Logic
      </button>
    </div>
  );
};
