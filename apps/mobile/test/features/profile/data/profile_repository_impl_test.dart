import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/profile/data/repositories/profile_repository_impl.dart';

void main() {
  late ProfileRepositoryImpl repository;

  setUp(() {
    repository = ProfileRepositoryImpl();
  });

  group('ProfileRepositoryImpl Unit Tests', () {
    test('getUserProfile returns user profile from remote data source', () async {
      final res = await repository.getUserProfile();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Failed to fetch profile'),
        (profile) => expect(profile.email, contains('@')),
      );
    });

    test('revokeSession returns true on success', () async {
      final res = await repository.revokeSession('sess_102');
      expect(res.isRight(), isTrue);
    });
  });
}
