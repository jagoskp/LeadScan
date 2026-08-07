export function formatScoreBadge(score: number): string {
  if (score >= 40) return '⭐ Exact Match';
  if (score >= 20) return '🔥 High Relevance';
  return 'Matched';
}
