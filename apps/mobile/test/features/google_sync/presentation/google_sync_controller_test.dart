import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/google_sync/data/repositories/google_sync_repository_impl.dart';
import 'package:leadscan_mobile/features/google_sync/presentation/controllers/google_sync_controller.dart';
import 'package:leadscan_mobile/features/google_sync/presentation/controllers/google_sync_state.dart';
import 'package:leadscan_mobile/features/google_sync/presentation/providers/google_sync_providers.dart';

void main() {
  late ProviderContainer container;
  late GoogleSyncController controller;

  setUp(() {
    final repository = GoogleSyncRepositoryImpl();
    container = ProviderContainer(
      overrides: [
        googleSyncRepositoryProvider.overrideWithValue(repository),
      ],
    );
    controller = container.read(googleSyncControllerProvider.notifier);
  });

  tearDown(() {
    container.dispose();
  });

  group('GoogleSyncController Unit Tests', () {
    test('initial state is accountSelection and fetches connected accounts', () async {
      expect(container.read(googleSyncControllerProvider).currentStep, equals(GoogleSyncStep.accountSelection));
      await controller.fetchAccounts();
      expect(container.read(googleSyncControllerProvider).accounts.isNotEmpty, isTrue);
    });

    test('proceedToSpreadsheetSelection updates step to spreadsheetBrowser', () async {
      await controller.fetchAccounts();
      await controller.proceedToSpreadsheetSelection();
      expect(container.read(googleSyncControllerProvider).currentStep, equals(GoogleSyncStep.spreadsheetBrowser));
      expect(container.read(googleSyncControllerProvider).spreadsheets.isNotEmpty, isTrue);
    });

    test('updateMapping modifies column mapping in state profile', () async {
      await controller.fetchAccounts();
      await controller.proceedToSpreadsheetSelection();
      await controller.proceedToWorksheetSelection();
      await controller.proceedToColumnDiscovery();

      expect(container.read(googleSyncControllerProvider).mappingProfile, isNotNull);
      controller.updateMapping('fullName', 'Full Name Custom Header');

      final state = container.read(googleSyncControllerProvider);
      final updatedItem = state.mappingProfile!.mappings.firstWhere((m) => m.sourceField == 'fullName');
      expect(updatedItem.targetColumn, equals('Full Name Custom Header'));
      expect(updatedItem.isAutoMapped, isFalse);
    });

    test('executeSync performs sync and transitions state to syncResult', () async {
      await controller.fetchAccounts();
      await controller.proceedToSpreadsheetSelection();
      await controller.proceedToWorksheetSelection();
      await controller.proceedToColumnDiscovery();
      await controller.proceedToSyncPreview();
      await controller.executeSync();

      final state = container.read(googleSyncControllerProvider);
      expect(state.currentStep, equals(GoogleSyncStep.syncResult));
      expect(state.syncResult, isNotNull);
      expect(state.syncResult!.status, equals('Success'));
    });
  });
}
