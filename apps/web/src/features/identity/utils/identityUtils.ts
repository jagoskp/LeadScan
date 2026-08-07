export function getConfidenceColor(level: string): string {
  switch (level) {
    case '100%':
      return '#10B981';
    case 'Very High':
      return '#059669';
    case 'High':
      return '#3B82F6';
    case 'Medium':
      return '#F59E0B';
    case 'Low':
      return '#EF4444';
    default:
      return '#6B7280';
  }
}
