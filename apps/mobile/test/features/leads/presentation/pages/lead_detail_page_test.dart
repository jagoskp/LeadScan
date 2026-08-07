import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/leads/presentation/pages/lead_detail_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('LeadDetailPage Widget Tests', () {
    testWidgets('renders lead profile details, sync CTA, and timeline', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const LeadDetailPage(leadId: 'lead_101')));
      await tester.pumpAndSettle();

      expect(find.text('Google Sync'), findsOneWidget);
      expect(find.text('Alex Morgan'), findsWidgets);
    });
  });
}
