import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/workflow/data/repositories/task_repository_impl.dart';
import 'package:leadscan_mobile/features/workflow/presentation/controllers/workflow_dashboard_controller.dart';
import 'package:leadscan_mobile/features/workflow/presentation/providers/workflow_providers.dart';

void main() {
  late ProviderContainer container;
  late WorkflowDashboardController controller;

  setUp(() {
    final repository = TaskRepositoryImpl();
    container = ProviderContainer(
      overrides: [
        taskRepositoryProvider.overrideWithValue(repository),
      ],
    );
    controller = container.read(workflowDashboardControllerProvider.notifier);
  });

  tearDown(() {
    container.dispose();
  });

  group('WorkflowDashboardController Unit Tests', () {
    test('initial state loads tasks and dashboard data', () async {
      await controller.loadDashboardData();
      final state = container.read(workflowDashboardControllerProvider);
      expect(state.tasks.isNotEmpty, isTrue);
    });

    test('setActiveTab updates activeTab in state', () {
      controller.setActiveTab('Agenda');
      final state = container.read(workflowDashboardControllerProvider);
      expect(state.activeTab, equals('Agenda'));
    });

    test('setSelectedFilter updates selectedFilter in state', () {
      controller.setSelectedFilter('Completed');
      final state = container.read(workflowDashboardControllerProvider);
      expect(state.selectedFilter, equals('Completed'));
    });
  });
}
