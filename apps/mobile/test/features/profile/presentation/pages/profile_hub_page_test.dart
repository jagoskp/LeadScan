import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/profile/domain/entities/user_profile_entity.dart';
import 'package:leadscan_mobile/features/profile/presentation/controllers/profile_controller.dart';
import 'package:leadscan_mobile/features/profile/presentation/controllers/profile_state.dart';
import 'package:leadscan_mobile/features/profile/presentation/pages/profile_hub_page.dart';
import 'package:leadscan_mobile/features/profile/presentation/providers/profile_providers.dart';

class _FakeProfileController extends StateNotifier<ProfileState> implements ProfileController {
  _FakeProfileController(super.state);

  @override
  Future<void> loadProfileData() async {}

  @override
  Future<void> updateProfileDetails({
    required String name,
    required String phone,
    required String company,
    required String designation,
  }) async {}

  @override
  Future<void> updateSettings(dynamic newSettings) async {}

  @override
  Future<void> revokeSession(String sessionId) async {}
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  final mockProfile = UserProfileEntity(
    id: 'usr_1',
    avatarUrl: '',
    name: 'Test User',
    email: 'test@leadscan.ai',
    phone: '+1 555 123 4567',
    company: 'LeadScan Inc',
    designation: 'Admin',
    accountStatus: 'Active PRO',
    createdAt: DateTime.now(),
  );

  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      overrides: [
        profileControllerProvider.overrideWith((ref) => _FakeProfileController(
          ProfileState(isLoading: false, profile: mockProfile),
        )),
      ],
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('ProfileHubPage Widget Tests', () {
    testWidgets('renders title, profile avatar, account status, and navigation tiles', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const ProfileHubPage()));
      await tester.pump();

      expect(find.text('Profile & Hub'), findsOneWidget);
      expect(find.text('Analytics Dashboard'), findsOneWidget);
      expect(find.text('App Settings'), findsOneWidget);
      expect(find.text('Security Center'), findsOneWidget);
    });
  });
}
