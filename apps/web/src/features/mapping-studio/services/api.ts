import { MappingRule } from "../types/studio";

export async function fetchMappingProfile(profileId: string): Promise<any> {
  const response = await fetch(`/api/mapping/profiles/${profileId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch mapping profile");
  }
  return response.json();
}

export async function saveMappingRules(
  profileId: string,
  rules: MappingRule[]
): Promise<boolean> {
  const response = await fetch(`/api/mapping/profiles/${profileId}/rules`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rules }),
  });
  return response.ok;
}

export async function getLivePreview(
  documentId: string,
  profileId: string
): Promise<any> {
  const response = await fetch("/api/mapping-studio/preview", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id: documentId, profile_id: profileId }),
  });
  if (!response.ok) {
    throw new Error("Failed to fetch DOM preview");
  }
  return response.json();
}
