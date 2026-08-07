export interface DOMEntity {
  id: string;
  type: string;
  value: string;
  confidence: number;
}

export interface TargetColumn {
  key: string;
  name: string;
  type: string;
  required: boolean;
}

export interface MappingRule {
  id: string;
  sourceEntityType: string;
  targetFieldName: string;
  fieldType: string;
  isRequired: boolean;
  defaultValue?: string;
}

export interface StudioState {
  profileId: string | null;
  documentId: string | null;
  rules: MappingRule[];
  selectedRuleId: string | null;
  isDragging: boolean;
  searchQuery: string;
}
