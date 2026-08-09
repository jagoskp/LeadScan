import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/profile/data/repositories/profile_repository_impl.dart';
import 'package:leadscan_mobile/features/profile/domain/usecases/get_analytics_usecase.dart';
import 'package:leadscan_mobile/features/profile/domain/usecases/get_profile_usecase.dart';
import 'package:leadscan_mobile/features/profile/domain/usecases/get_security_info_usecase.dart';
import 'package:leadscan_mobile/features/profile/domain/usecases/get_settings_usecase.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late ProfileRepositoryImpl repository;
  late GetProfileUseCase getProfileUseCase;
  late GetAnalyticsUseCase getAnalyticsUseCase;
  late GetSettingsUseCase getSettingsUseCase;
  late GetSecurityInfoUseCase getSecurityInfoUseCase;

  setUp(() {
    FlutterSecureStorage.setMockInitialValues({'auth_user_name': 'Test User', 'auth_user_email': 'test@leadscan.ai'});
    repository = ProfileRepositoryImpl();
    getProfileUseCase = GetProfileUseCase(repository);
    getAnalyticsUseCase = GetAnalyticsUseCase(repository);
    getSettingsUseCase = GetSettingsUseCase(repository);
    getSecurityInfoUseCase = GetSecurityInfoUseCase(repository);
  });

  group('Profile UseCases Unit Tests', () {
    test('GetProfileUseCase returns user profile', () async {
      final res = await getProfileUseCase();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (profile) => expect(profile.name, isNotEmpty),
      );
    });

    test('GetAnalyticsUseCase returns analytics metrics', () async {
      final res = await getAnalyticsUseCase();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (analytics) => expect(analytics.totalLeads, greaterThan(0)),
      );
    });

    test('GetSettingsUseCase returns user settings', () async {
      final res = await getSettingsUseCase();
      expect(res.isRight(), isTrue);
    });

    test('GetSecurityInfoUseCase returns security info', () async {
      final res = await getSecurityInfoUseCase();
      expect(res.isRight(), isTrue);
    });
  });
}
