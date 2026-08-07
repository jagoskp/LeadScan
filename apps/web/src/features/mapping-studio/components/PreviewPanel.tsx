import React from "react";

interface PreviewPanelProps {
  previewData: any;
  loading: boolean;
}

export const PreviewPanel: React.FC<PreviewPanelProps> = ({
  previewData,
  loading,
}) => {
  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl">
      <h3 className="text-lg font-bold text-white mb-4">Live Preview</h3>
      {loading ? (
        <p className="text-slate-500 text-sm">Computing live preview values...</p>
      ) : !previewData ? (
        <p className="text-slate-500 text-sm">No preview generated yet.</p>
      ) : (
        <div className="space-y-4">
          <div>
            <span className="text-xs font-semibold text-slate-500 block mb-1">
              Mapped Outcomes
            </span>
            <div className="space-y-2">
              {previewData.mapped_results.map((res: any, i: number) => (
                <div key={i} className="flex justify-between text-sm">
                  <span className="text-slate-400">{res.field_name}:</span>
                  <span className="text-white font-medium">{res.value}</span>
                </div>
              ))}
            </div>
          </div>
          {previewData.unmapped_fields.length > 0 && (
            <div>
              <span className="text-xs font-semibold text-slate-500 block mb-1">
                Unmapped Elements
              </span>
              <div className="space-y-1">
                {previewData.unmapped_fields.map((unm: any, i: number) => (
                  <div key={i} className="text-sm text-amber-500">
                    {unm.raw_text}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
