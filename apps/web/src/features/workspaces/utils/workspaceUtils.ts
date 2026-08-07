export function getRoleBadgeColor(role: string): string {
  switch (role) {
    case 'Owner':
      return '#8B5CF6';
    case 'Admin':
      return '#EF4444';
    case 'Manager':
      return '#F59E0B';
    case 'Operator':
      return '#3B82F6';
    case 'Reviewer':
      return '#10B981';
    case 'Viewer':
      return '#6B7280';
    default:
      return '#6B7280';
  }
}
