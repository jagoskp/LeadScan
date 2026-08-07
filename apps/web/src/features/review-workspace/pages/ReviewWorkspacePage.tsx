import React, { useState } from "react";
import { useReviewWorkspace } from "../hooks/useReviewWorkspace";
import { ReviewCanvas } from "../components/ReviewCanvas";
import { CorrectionForm } from "../components/CorrectionForm";
import { ImagePreview } from "../components/ImagePreview";
import { submitItemCorrection, approveSession } from "../services/api";
import { ReviewSession } from "../types/review";

const mockSession: ReviewSession = {
  id: "session-123",
  documentId: "doc-123",
  status: "Pending",
  items: [
    {
      id: "item-1",
      fieldName: "company_name",
      originalValue: "LeadScan AI Corp.",
      currentValue: "LeadScan AI Corp.",
      confidenceScore: 0.99,
      confidenceLevel: "High",
      isExtraInfo: false,
      status: "Pending",
    },
    {
      id: "item-2",
      fieldName: "contact_phone",
      originalValue: "+1-555-0199",
      currentValue: "+1-555-0199",
      confidenceScore: 0.85,
      confidenceLevel: "Medium",
      isExtraInfo: false,
      status: "Pending",
    },
  ],
  validationIssues: [],
};

export const ReviewWorkspacePage: React.FC = () => {
  const {
    session,
    selectedItemId,
    setSelectedItemId,
    confidenceFilter,
    setConfidenceFilter,
    updateItemValue,
    filteredItems,
  } = useReviewWorkspace(mockSession);

  const [saving, setSaving] = useState(false);

  const selectedItem =
    session?.items.find((item) => item.id === selectedItemId) || null;

  const handleApplyCorrection = async (
    itemId: string,
    val: string,
    reason: string
  ) => {
    setSaving(true);
    try {
      await submitItemCorrection(itemId, val, reason);
      updateItemValue(itemId, val);
    } catch {
      // Stub error fallback
      updateItemValue(itemId, val);
    } finally {
      setSaving(false);
    }
  };

  const handleApproveSession = async () => {
    if (!session) return;
    await approveSession(session.id);
  };

  return (
    <div className="min-h-screen bg-slate-950 p-8 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Review Workspace</h1>
          <p className="text-slate-400 text-sm">
            Correct OCR extraction results, validate formatting, and approve leads.
          </p>
        </div>
        <button
          onClick={handleApproveSession}
          className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-lg transition"
        >
          Approve and Lock Leads
        </button>
      </div>

      <div className="flex gap-4">
        <button
          onClick={() => setConfidenceFilter(null)}
          className={`px-3 py-1 text-xs rounded font-semibold ${
            !confidenceFilter ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400"
          }`}
        >
          All Confidences
        </button>
        <button
          onClick={() => setConfidenceFilter("Low")}
          className={`px-3 py-1 text-xs rounded font-semibold ${
            confidenceFilter === "Low" ? "bg-rose-600 text-white" : "bg-slate-800 text-slate-400"
          }`}
        >
          Low Confidence Only
        </button>
      </div>

      <div className="flex gap-6">
        <ReviewCanvas
          items={filteredItems}
          selectedItemId={selectedItemId}
          onSelectItem={setSelectedItemId}
        />
        <CorrectionForm
          item={selectedItem}
          onSaveCorrection={handleApplyCorrection}
        />
      </div>

      <ImagePreview imageUrl="file:///path/to/mock/image.png" />
    </div>
  );
};
export default ReviewWorkspacePage;
