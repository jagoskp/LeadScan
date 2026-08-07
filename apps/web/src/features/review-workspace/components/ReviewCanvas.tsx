import React from "react";
import { ReviewItem } from "../types/review";

interface ReviewCanvasProps {
  items: ReviewItem[];
  selectedItemId: string | null;
  onSelectItem: (id: string) => void;
}

export const ReviewCanvas: React.FC<ReviewCanvasProps> = ({
  items,
  selectedItemId,
  onSelectItem,
}) => {
  return (
    <div className="flex-1 p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
      <h2 className="text-xl font-bold text-white">Review Canvas</h2>
      <div className="space-y-3">
        {items.map((item) => (
          <div
            key={item.id}
            onClick={() => onSelectItem(item.id)}
            className={`flex justify-between items-center p-3 border rounded-lg hover:border-violet-500 cursor-pointer transition ${
              selectedItemId === item.id
                ? "bg-slate-800 border-violet-500"
                : "bg-slate-800 border-slate-700"
            }`}
          >
            <div>
              <span className="text-xs font-semibold text-slate-400 block uppercase">
                {item.fieldName}
              </span>
              <span className="text-sm text-white font-medium">
                {item.currentValue || "(Empty)"}
              </span>
            </div>
            <div className="flex items-center gap-3">
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                  item.confidenceLevel === "High"
                    ? "bg-emerald-500/10 text-emerald-400"
                    : item.confidenceLevel === "Medium"
                    ? "bg-amber-500/10 text-amber-400"
                    : "bg-rose-500/10 text-rose-400"
                }`}
              >
                {item.confidenceLevel}
              </span>
              {item.isExtraInfo && (
                <span className="text-[10px] bg-slate-700 text-slate-300 px-1.5 py-0.5 rounded font-mono">
                  Extra Info
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
