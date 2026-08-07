import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/review/presentation/pages/review_workspace_page.dart';

void main() {
  Widget buildTestableWidget() {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: const ReviewWorkspacePage(),
      ),
    );
  }

  group('ReviewWorkspacePage Widget Tests', () {
    testWidgets('renders workspace title, tab buttons, editable form, and approve button', (tester) async {
      await tester.pumpWidget(buildTestableWidget());
      await tester.pump();

      expect(find.text('AI Review Workspace'), findsOneWidget);
      expect(find.text('Smart Editable Form'), findsOneWidget);
      expect(find.text('Compare Card vs OCR'), findsOneWidget);

      await tester.pump(const Duration(milliseconds: 500));

      expect(find.text('Approve & Validate'), findsOneWidget);
      expect(find.text('Alex Morgan'), findsWidgets);
    });
  });
}
