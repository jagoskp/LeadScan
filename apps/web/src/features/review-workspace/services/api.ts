export async function fetchReviewSession(sessionId: string): Promise<any> {
  const response = await fetch(`/api/review/sessions/${sessionId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch review session details");
  }
  return response.json();
}

export async function submitItemCorrection(
  itemId: string,
  currentValue: string,
  reason?: string
): Promise<any> {
  const response = await fetch(`/api/review/items/${itemId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ current_value: currentValue, reason }),
  });
  if (!response.ok) {
    throw new Error("Failed to submit manual correction");
  }
  return response.json();
}

export async function approveSession(sessionId: string): Promise<boolean> {
  const response = await fetch(`/api/review/sessions/${sessionId}/approve`, {
    method: "POST",
  });
  return response.ok;
}
