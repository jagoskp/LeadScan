export interface ReviewItem {
  id: string;
  fieldName: string;
  originalValue: string | null;
  currentValue: string | null;
  confidenceScore: number | null;
  confidenceLevel: "High" | "Medium" | "Low";
  isExtraInfo: boolean;
  status: "Pending" | "Approved" | "Rejected";
}

export interface ValidationIssue {
  id: string;
  fieldName: string;
  issueType: string;
  message: string;
}

export interface ReviewSession {
  id: string;
  documentId: string;
  status: "Pending" | "Approved" | "Rejected";
  items: ReviewItem[];
  validationIssues: ValidationIssue[];
}
