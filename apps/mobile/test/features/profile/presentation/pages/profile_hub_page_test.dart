import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/profile/presentation/pages/profile_hub_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('ProfileHubPage Widget Tests', () {
    testWidgets('renders title, profile avatar, account status, and navigation tiles', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const ProfileHubPage()));
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pumpAndSettle();

      expect(find.text('Profile & Hub'), findsOneWidget);
      expect(find.text('Analytics Dashboard'), findsOneWidget);
      expect(find.text('App Settings'), findsOneWidget);
      expect(find.text('Security Center'), findsOneWidget);
    });
  });
}
