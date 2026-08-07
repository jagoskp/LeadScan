import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/profile/presentation/pages/security_center_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('SecurityCenterPage Widget Tests', () {
    testWidgets('renders title, active sessions, and app security settings', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const SecurityCenterPage()));
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pumpAndSettle();

      expect(find.text('Security Center'), findsOneWidget);
      expect(find.text('Active Sessions & Devices'), findsOneWidget);
      expect(find.text('Biometric Authentication'), findsOneWidget);
    });
  });
}
