import React, { useState, useEffect } from "react";
import { ReviewItem } from "../types/review";

interface CorrectionFormProps {
  item: ReviewItem | null;
  onSaveCorrection: (itemId: string, val: string, reason: string) => void;
}

export const CorrectionForm: React.FC<CorrectionFormProps> = ({
  item,
  onSaveCorrection,
}) => {
  const [val, setVal] = useState("");
  const [reason, setReason] = useState("");

  useEffect(() => {
    if (item) {
      setVal(item.currentValue || "");
      setReason("");
    }
  }, [item]);

  if (!item) {
    return (
      <div className="w-80 p-6 bg-slate-900 border border-slate-800 rounded-xl">
        <h3 className="text-lg font-bold text-white mb-2">Correction Panel</h3>
        <p className="text-slate-500 text-sm">Select an item from the canvas to edit.</p>
      </div>
    );
  }

  return (
    <div className="w-80 p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
      <h3 className="text-lg font-bold text-white">Correction Panel</h3>
      <div>
        <label className="text-xs font-semibold text-slate-400 block mb-1">
          Field: {item.fieldName}
        </label>
        <input
          type="text"
          value={val}
          onChange={(e) => setVal(e.target.value)}
          className="w-full bg-slate-800 border border-slate-700 text-white rounded p-2 text-sm focus:outline-none focus:border-violet-500"
        />
      </div>
      <div>
        <label className="text-xs font-semibold text-slate-400 block mb-1">
          Reason for Correction
        </label>
        <input
          type="text"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="e.g. Typo fix"
          className="w-full bg-slate-800 border border-slate-700 text-white rounded p-2 text-sm focus:outline-none focus:border-violet-500"
        />
      </div>
      <button
        onClick={() => onSaveCorrection(item.id, val, reason)}
        className="w-full bg-violet-600 hover:bg-violet-700 text-white font-semibold rounded p-2 text-sm transition"
      >
        Apply Correction
      </button>
    </div>
  );
};
