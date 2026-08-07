import React from "react";
import { MappingRule } from "../types/studio";

interface MappingCanvasProps {
  rules: MappingRule[];
  onRemoveRule: (id: string) => void;
  onSelectRule: (id: string) => void;
}

export const MappingCanvas: React.FC<MappingCanvasProps> = ({
  rules,
  onRemoveRule,
  onSelectRule,
}) => {
  return (
    <div className="flex-1 p-6 bg-slate-900 border border-slate-800 rounded-xl">
      <h2 className="text-xl font-bold text-white mb-4">Mapping Canvas</h2>
      {rules.length === 0 ? (
        <p className="text-slate-500 text-sm">
          Drag source entities here to map them to target columns.
        </p>
      ) : (
        <div className="space-y-3">
          {rules.map((rule) => (
            <div
              key={rule.id}
              onClick={() => onSelectRule(rule.id)}
              className="flex justify-between items-center p-3 bg-slate-800 border border-slate-700 rounded-lg hover:border-violet-500 cursor-pointer transition"
            >
              <div>
                <span className="text-xs font-semibold text-violet-400 uppercase">
                  {rule.sourceEntityType}
                </span>
                <span className="mx-2 text-slate-500">→</span>
                <span className="text-sm text-white font-medium">
                  {rule.targetFieldName}
                </span>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onRemoveRule(rule.id);
                }}
                className="text-slate-400 hover:text-red-500 text-sm font-semibold"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
