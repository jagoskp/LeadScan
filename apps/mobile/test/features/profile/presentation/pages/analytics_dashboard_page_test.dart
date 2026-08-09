import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/profile/data/datasources/profile_remote_datasource.dart';
import 'package:leadscan_mobile/features/profile/presentation/pages/analytics_dashboard_page.dart';
import 'package:leadscan_mobile/features/profile/presentation/providers/profile_providers.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({'auth_user_name': 'Test User', 'auth_user_email': 'test@leadscan.ai'});

  // Use a shared storage that all layers in tests reference
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

  group('AnalyticsDashboardPage Widget Tests', () {
    testWidgets('renders title and KPI metric cards grid', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const AnalyticsDashboardPage()));
      await tester.pump(const Duration(milliseconds: 500));

      expect(find.text('Admin & Activity Dashboard'), findsOneWidget);
      expect(find.text('Leads Created'), findsOneWidget);
      expect(find.text('Sheets Sync Count'), findsOneWidget);
    });
  });
}
