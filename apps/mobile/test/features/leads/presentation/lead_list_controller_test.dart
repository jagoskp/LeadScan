import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/leads/data/repositories/lead_repository_impl.dart';
import 'package:leadscan_mobile/features/leads/presentation/controllers/lead_list_controller.dart';
import 'package:leadscan_mobile/features/leads/presentation/providers/lead_providers.dart';

void main() {
  late ProviderContainer container;
  late LeadListController controller;

  setUp(() {
    final repository = LeadRepositoryImpl();
    container = ProviderContainer(
      overrides: [
        leadRepositoryProvider.overrideWithValue(repository),
      ],
    );
    controller = container.read(leadListControllerProvider.notifier);
  });

  tearDown(() {
    container.dispose();
  });

  group('LeadListController Unit Tests', () {
    test('initial state loads leads from repository', () async {
      await controller.fetchLeads();
      final state = container.read(leadListControllerProvider);
      expect(state.leads.isNotEmpty, isTrue);
    });

    test('setSearchQuery updates filter options and filters leads', () async {
      await controller.setSearchQuery('Alex');
      final state = container.read(leadListControllerProvider);
      expect(state.filterOptions.searchQuery, equals('Alex'));
      expect(state.leads.length, equals(1));
    });

    test('toggleLeadSelection manages selectedLeadIds and isBulkSelectionMode', () {
      controller.toggleLeadSelection('lead_101');
      var state = container.read(leadListControllerProvider);
      expect(state.selectedLeadIds.contains('lead_101'), isTrue);
      expect(state.isBulkSelectionMode, isTrue);

      controller.clearSelection();
      state = container.read(leadListControllerProvider);
      expect(state.selectedLeadIds.isEmpty, isTrue);
      expect(state.isBulkSelectionMode, isFalse);
    });
  });
}
