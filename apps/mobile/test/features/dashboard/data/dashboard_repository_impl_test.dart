import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:leadscan_mobile/features/auth/data/models/user_model.dart';
import 'package:leadscan_mobile/features/dashboard/data/repositories/dashboard_repository_impl.dart';
import 'package:leadscan_mobile/features/profile/data/datasources/profile_remote_datasource.dart';
import 'package:leadscan_mobile/features/profile/data/repositories/profile_repository_impl.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({});

  group('Secure Storage & User Identity Unit Tests', () {
    final storage = const FlutterSecureStorage(
      aOptions: AndroidOptions(encryptedSharedPreferences: true),
    );
    final localDataSource = AuthLocalDataSourceImpl(storage: storage);
    final dashboardRepo = DashboardRepositoryImpl(storage: storage);
    final profileRepo = ProfileRepositoryImpl(
      remoteDataSource: ProfileRemoteDataSourceImpl(storage: storage),
    );

    setUp(() async {
      await storage.deleteAll();
    });

    test('Test 1: Auth saves Rahul Sharma & rahul@gmail.com -> Dashboard reads Rahul Sharma', () async {
      await localDataSource.saveUser(const UserModel(
        id: 'usr_1',
        name: 'Rahul Sharma',
        email: 'rahul@gmail.com',
      ));

      final result = await dashboardRepo.getDashboardSummary();
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Failed'),
        (summary) => expect(summary.userName, 'Rahul Sharma'),
      );
    });

    test('Test 2: Name empty/null -> Dashboard reads rahul@gmail.com', () async {
      await localDataSource.saveUser(const UserModel(
        id: 'usr_2',
        name: '',
        email: 'rahul@gmail.com',
      ));

      final result = await dashboardRepo.getDashboardSummary();
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Failed'),
        (summary) => expect(summary.userName, 'rahul@gmail.com'),
      );
    });

    test('Test 3: Profile reads the same identity matching Auth storage', () async {
      await localDataSource.saveUser(const UserModel(
        id: 'usr_3',
        name: 'Rahul Sharma',
        email: 'rahul@gmail.com',
      ));

      final result = await profileRepo.getUserProfile();
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Failed'),
        (profile) {
          expect(profile.name, 'Rahul Sharma');
          expect(profile.email, 'rahul@gmail.com');
        },
      );
    });

    test('Test 4: Account A login -> Dashboard & Profile show Account A', () async {
      await localDataSource.saveUser(const UserModel(
        id: 'usr_A',
        name: 'Account A',
        email: 'accountA@gmail.com',
      ));

      final dashRes = await dashboardRepo.getDashboardSummary();
      dashRes.fold((l) => fail('Failed'), (s) => expect(s.userName, 'Account A'));

      final profRes = await profileRepo.getUserProfile();
      profRes.fold((l) => fail('Failed'), (p) => expect(p.name, 'Account A'));
    });

    test('Test 5: Logout clears Account A identity from storage', () async {
      await localDataSource.saveUser(const UserModel(
        id: 'usr_A',
        name: 'Account A',
        email: 'accountA@gmail.com',
      ));
      await localDataSource.clearUser();

      final dashRes = await dashboardRepo.getDashboardSummary();
      dashRes.fold((l) => fail('Failed'), (s) => expect(s.userName, 'User'));

      final profRes = await profileRepo.getUserProfile();
      profRes.fold((l) => fail('Failed'), (p) => expect(p.name, 'User'));
    });

    test('Test 6: Account B login -> Dashboard & Profile show Account B without stale Account A identity', () async {
      // Account A
      await localDataSource.saveUser(const UserModel(
        id: 'usr_A',
        name: 'Account A',
        email: 'accountA@gmail.com',
      ));

      // Logout
      await localDataSource.clearUser();

      // Account B
      await localDataSource.saveUser(const UserModel(
        id: 'usr_B',
        name: 'Account B',
        email: 'accountB@gmail.com',
      ));

      final dashRes = await dashboardRepo.getDashboardSummary();
      dashRes.fold((l) => fail('Failed'), (s) => expect(s.userName, 'Account B'));

      final profRes = await profileRepo.getUserProfile();
      profRes.fold((l) => fail('Failed'), (p) {
        expect(p.name, 'Account B');
        expect(p.email, 'accountB@gmail.com');
      });
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
