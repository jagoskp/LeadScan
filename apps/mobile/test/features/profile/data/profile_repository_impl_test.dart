import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/profile/data/repositories/profile_repository_impl.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({'auth_user_name': 'Rahul Sharma', 'auth_user_email': 'rahul@gmail.com'});

  late ProfileRepositoryImpl repository;

  setUp(() {
    repository = ProfileRepositoryImpl();
  });

  group('ProfileRepositoryImpl Unit Tests', () {
    test('getUserProfile returns user profile matching stored identity', () async {
      final res = await repository.getUserProfile();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Failed to fetch profile'),
        (profile) {
          expect(profile.name, 'Rahul Sharma');
          expect(profile.email, 'rahul@gmail.com');
        },
      );
    });

    test('updateProfile persists name, phone, company, designation to secure storage', () async {
      final initialRes = await repository.getUserProfile();
      final current = initialRes.getOrElse(() => throw Exception());

      final updatedEntity = current.copyWith(
        name: 'Rahul Sharma Updated',
        phone: '9876543210',
        company: 'ABC Tech',
        designation: 'VP Sales',
      );

      final updateRes = await repository.updateProfile(updatedEntity);
      expect(updateRes.isRight(), isTrue);

      final freshProfileRes = await repository.getUserProfile();
      final fresh = freshProfileRes.getOrElse(() => throw Exception());
      expect(fresh.name, equals('Rahul Sharma Updated'));
      expect(fresh.phone, equals('9876543210'));
      expect(fresh.company, equals('ABC Tech'));
      expect(fresh.designation, equals('VP Sales'));
    });

    test('Account A and Account B profile isolation on storage wipe', () async {
      // Account A profile setup
      FlutterSecureStorage.setMockInitialValues({
        'auth_user_name': 'Account A User',
        'auth_user_email': 'accountA@gmail.com',
        'auth_user_company': 'Company A',
      });
      final repoA = ProfileRepositoryImpl();
      final resA = (await repoA.getUserProfile()).getOrElse(() => throw Exception());
      expect(resA.name, equals('Account A User'));
      expect(resA.company, equals('Company A'));

      // Logout Account A (wipes storage) -> Account B login
      FlutterSecureStorage.setMockInitialValues({
        'auth_user_name': 'Account B User',
        'auth_user_email': 'accountB@gmail.com',
        'auth_user_company': 'Company B',
      });
      final repoB = ProfileRepositoryImpl();
      final resB = (await repoB.getUserProfile()).getOrElse(() => throw Exception());
      expect(resB.name, equals('Account B User'));
      expect(resB.company, equals('Company B'));

      // Account B profile never contains Account A data
      expect(resB.email, isNot(equals('accountA@gmail.com')));
    });

    test('revokeSession returns true on success', () async {
      final res = await repository.revokeSession('sess_102');
      expect(res.isRight(), isTrue);
    });
  });
}
