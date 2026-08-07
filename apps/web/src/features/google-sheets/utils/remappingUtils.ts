export function formatRemappingReason(score: number): string {
  if (score >= 0.95) return 'Exact Synonym Match';
  if (score >= 0.8) return 'High Similarity Score';
  return 'Potential Fuzzy Match';
}
