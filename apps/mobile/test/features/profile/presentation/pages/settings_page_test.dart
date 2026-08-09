import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/profile/data/datasources/profile_remote_datasource.dart';
import 'package:leadscan_mobile/features/profile/presentation/pages/settings_page.dart';
import 'package:leadscan_mobile/features/profile/presentation/providers/profile_providers.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({'auth_user_name': 'Test User'});

  final storage = const FlutterSecureStorage();

  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      // Override profileRemoteDataSourceProvider to avoid GetIt registration
      overrides: [
        profileRemoteDataSourceProvider.overrideWith(
          (ref) => ProfileRemoteDataSourceImpl(storage: storage),
        ),
      ],
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('SettingsPage Widget Tests', () {
    testWidgets('renders title, theme options, and preferences toggles', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const SettingsPage()));
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pumpAndSettle();

      expect(find.text('App Settings'), findsOneWidget);
      expect(find.text('Appearance & Theme'), findsOneWidget);
      expect(find.text('Push Notifications'), findsOneWidget);
    });
  });
}
