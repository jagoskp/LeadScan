import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/profile/presentation/pages/analytics_dashboard_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('AnalyticsDashboardPage Widget Tests', () {
    testWidgets('renders title and KPI metric cards grid', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const AnalyticsDashboardPage()));
      await tester.pumpAndSettle();

      expect(find.text('Analytics Dashboard'), findsOneWidget);
      expect(find.text('Total Leads'), findsOneWidget);
      expect(find.text('OCR Accuracy'), findsOneWidget);
    });
  });
}
