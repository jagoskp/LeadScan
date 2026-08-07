export function getPriorityBadgeColor(priority: string): string {
  switch (priority) {
    case 'High':
      return '#EF4444';
    case 'Medium':
      return '#F59E0B';
    case 'Low':
      return '#10B981';
    default:
      return '#6B7280';
  }
}
