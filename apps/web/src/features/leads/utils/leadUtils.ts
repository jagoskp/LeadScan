export function getStatusColor(status: string): string {
  switch (status) {
    case 'New':
      return '#3B82F6';
    case 'Contacted':
      return '#8B5CF6';
    case 'Qualified':
      return '#F59E0B';
    case 'Interested':
      return '#EC4899';
    case 'Proposal':
      return '#6366F1';
    case 'Won':
      return '#10B981';
    case 'Lost':
      return '#EF4444';
    case 'Archived':
      return '#6B7280';
    default:
      return '#3B82F6';
  }
}
