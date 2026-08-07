import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/google_sync/data/repositories/google_sync_repository_impl.dart';
import 'package:leadscan_mobile/features/google_sync/domain/entities/column_mapping_entity.dart';

void main() {
  late GoogleSyncRepositoryImpl repository;

  setUp(() {
    repository = GoogleSyncRepositoryImpl();
  });

  group('GoogleSyncRepositoryImpl Unit Tests', () {
    test('getConnectedAccounts returns Right with GoogleAccountEntity list', () async {
      final result = await repository.getConnectedAccounts();
      expect(result.isRight(), isTrue);
    });

    test('getSpreadsheets returns list of spreadsheets', () async {
      final result = await repository.getSpreadsheets('acc_01');
      expect(result.isRight(), isTrue);
    });

    test('getWorksheets returns list of worksheets', () async {
      final result = await repository.getWorksheets('acc_01', 'sheet_01');
      expect(result.isRight(), isTrue);
    });

    test('performGoogleSync executes sync and returns SyncResultEntity', () async {
      final mappingProfile = ColumnMappingProfileEntity(
        id: 'prof_1',
        spreadsheetId: 'sheet_01',
        worksheetTitle: 'Sheet1',
        mappings: const [
          ColumnMappingItem(sourceField: 'fullName', sourceFieldLabel: 'Full Name', targetColumn: 'Full Name'),
        ],
        updatedAt: DateTime.now(),
      );

      final result = await repository.performGoogleSync(
        accountId: 'acc_01',
        spreadsheetId: 'sheet_01',
        worksheetTitle: 'Sheet1',
        mappingProfile: mappingProfile,
        leadData: {'fullName': 'Alex Morgan'},
      );

      expect(result.isRight(), isTrue);
      result.fold(
        (failure) => fail('Sync execution failed'),
        (syncRes) {
          expect(syncRes.status, equals('Success'));
          expect(syncRes.totalRows, equals(1));
        },
      );
    });
  });
}
