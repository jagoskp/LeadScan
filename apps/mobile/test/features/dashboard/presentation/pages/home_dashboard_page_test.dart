import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:leadscan_mobile/features/dashboard/domain/entities/dashboard_summary_entity.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/controllers/dashboard_controller.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/controllers/dashboard_state.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/pages/home_dashboard_page.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/providers/dashboard_providers.dart';

class _FakeDashboardController extends StateNotifier<DashboardState> implements DashboardController {
  _FakeDashboardController(super.state);

  @override
  Future<void> fetchDashboardSummary() async {}

  @override
  Future<void> refresh() async {}
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  GoogleFonts.config.allowRuntimeFetching = false;

  group('HomeDashboardPage Widget Tests', () {
    testWidgets('renders top bar with userName', (tester) async {
      final mockState = DashboardState(
        status: DashboardStatus.success,
        summary: const DashboardSummaryEntity(
          userName: 'Alex Morgan',
          userAvatarUrl: null,
          unreadNotificationsCount: 0,
          totalLeads: KpiMetricEntity(title: 'Total', value: '10', trendLabel: 'Up', isTrendPositive: true),
          todaysLeads: KpiMetricEntity(title: 'Today', value: '2', trendLabel: 'Up', isTrendPositive: true),
          pendingFollowups: KpiMetricEntity(title: 'Pending', value: '1', trendLabel: 'Up', isTrendPositive: true),
          googleSyncStatus: KpiMetricEntity(title: 'Sync', value: 'OK', trendLabel: 'Up', isTrendPositive: true),
          aiInsights: [],
          workflowSummary: WorkflowSummaryEntity(todaysTasksCount: 0, upcomingFollowupsCount: 0, completedTodayCount: 0),
          recentLeads: [],
        ),
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            dashboardControllerProvider.overrideWith((ref) => _FakeDashboardController(mockState)),
          ],
          child: const MaterialApp(
            home: HomeDashboardPage(),
          ),
        ),
      );

      await tester.pump();
      await tester.pumpAndSettle();

      expect(find.text('Good morning 👋'), findsOneWidget);
      expect(find.text('Alex Morgan'), findsOneWidget);
    });
  });
}
