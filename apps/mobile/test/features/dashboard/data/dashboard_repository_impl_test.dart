import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/dashboard/data/repositories/dashboard_repository_impl.dart';

void main() {
  group('DashboardRepositoryImpl Unit Tests', () {
    test('getDashboardSummary returns DashboardSummaryEntity on success', () async {
      final repository = DashboardRepositoryImpl();
      final result = await repository.getDashboardSummary();

      expect(result.isRight(), isTrue);
      result.fold(
        (failure) => fail('Should not fail'),
        (summary) {
          expect(summary.userName, 'Alex Morgan');
          expect(summary.unreadNotificationsCount, 3);
          expect(summary.totalLeads.value, '1,248');
          expect(summary.todaysLeads.value, '24');
          expect(summary.aiInsights.length, 3);
          expect(summary.recentLeads.length, 3);
        },
      );
    });

    test('getDashboardSummary returns Failure when shouldFail is true', () async {
      final repository = DashboardRepositoryImpl(shouldFail: true);
      final result = await repository.getDashboardSummary();

      expect(result.isLeft(), isTrue);
      result.fold(
        (failure) => expect(failure.message, 'Failed to fetch dashboard data'),
        (_) => fail('Should have failed'),
      );
    });
  });
}
