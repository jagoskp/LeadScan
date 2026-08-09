import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/profile/data/repositories/profile_repository_impl.dart';
import 'package:leadscan_mobile/features/profile/presentation/controllers/profile_controller.dart';
import 'package:leadscan_mobile/features/profile/presentation/providers/profile_providers.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late ProviderContainer container;
  late ProfileController controller;

  setUp(() {
    FlutterSecureStorage.setMockInitialValues({'auth_user_name': 'Test User', 'auth_user_email': 'test@leadscan.ai'});
    final repository = ProfileRepositoryImpl();
    container = ProviderContainer(
      overrides: [
        profileRepositoryProvider.overrideWithValue(repository),
      ],
    );
    controller = container.read(profileControllerProvider.notifier);
  });

  tearDown(() {
    container.dispose();
  });

  group('ProfileController Unit Tests', () {
    test('initial state loads profile, analytics, settings and security info', () async {
      await controller.loadProfileData();
      final state = container.read(profileControllerProvider);
      expect(state.profile, isNotNull);
      expect(state.analytics, isNotNull);
    });

    test('updateProfileDetails updates profile state', () async {
      await controller.loadProfileData();
      await controller.updateProfileDetails(
        name: 'Updated Name',
        phone: '+1 555 999 8888',
        company: 'Updated Co',
        designation: 'VP',
      );
      final state = container.read(profileControllerProvider);
      expect(state.profile?.name, equals('Updated Name'));
    });
  });
}
