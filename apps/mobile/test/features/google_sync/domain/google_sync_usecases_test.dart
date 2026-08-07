import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/google_sync/data/repositories/google_sync_repository_impl.dart';
import 'package:leadscan_mobile/features/google_sync/domain/usecases/get_connected_accounts_usecase.dart';
import 'package:leadscan_mobile/features/google_sync/domain/usecases/get_sheet_columns_usecase.dart';
import 'package:leadscan_mobile/features/google_sync/domain/usecases/get_spreadsheets_usecase.dart';
import 'package:leadscan_mobile/features/google_sync/domain/usecases/get_worksheets_usecase.dart';

void main() {
  late GoogleSyncRepositoryImpl repository;
  late GetConnectedAccountsUseCase getAccountsUseCase;
  late GetSpreadsheetsUseCase getSheetsUseCase;
  late GetWorksheetsUseCase getWorksheetsUseCase;
  late GetSheetColumnsUseCase getColumnsUseCase;

  setUp(() {
    repository = GoogleSyncRepositoryImpl();
    getAccountsUseCase = GetConnectedAccountsUseCase(repository);
    getSheetsUseCase = GetSpreadsheetsUseCase(repository);
    getWorksheetsUseCase = GetWorksheetsUseCase(repository);
    getColumnsUseCase = GetSheetColumnsUseCase(repository);
  });

  group('Google Sync UseCases Unit Tests', () {
    test('GetConnectedAccountsUseCase returns list of accounts', () async {
      final res = await getAccountsUseCase();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (accounts) {
          expect(accounts.isNotEmpty, isTrue);
          expect(accounts.first.email, contains('@'));
        },
      );
    });

    test('GetSpreadsheetsUseCase returns spreadsheets for account', () async {
      final res = await getSheetsUseCase('acc_01');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (sheets) {
          expect(sheets.isNotEmpty, isTrue);
          expect(sheets.first.title, isNotEmpty);
        },
      );
    });

    test('GetWorksheetsUseCase returns worksheets for spreadsheet', () async {
      final res = await getWorksheetsUseCase('acc_01', 'sheet_01');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (worksheets) {
          expect(worksheets.isNotEmpty, isTrue);
        },
      );
    });

    test('GetSheetColumnsUseCase returns column headers', () async {
      final res = await getColumnsUseCase('acc_01', 'sheet_01', 'Sheet1');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (columns) {
          expect(columns.isNotEmpty, isTrue);
        },
      );
    });
  });
}
