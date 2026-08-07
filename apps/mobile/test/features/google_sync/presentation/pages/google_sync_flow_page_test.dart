import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/google_sync/presentation/pages/google_sync_flow_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('GoogleSyncFlowPage Widget Tests', () {
    testWidgets('renders app bar title and initial account selection step', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const GoogleSyncFlowPage()));
      await tester.pumpAndSettle();

      expect(find.text('Google Sheets Mapping Studio'), findsOneWidget);
      expect(find.text('Select Connected Google Account'), findsOneWidget);
      expect(find.text('Select Spreadsheet'), findsOneWidget);
    });
  });
}
