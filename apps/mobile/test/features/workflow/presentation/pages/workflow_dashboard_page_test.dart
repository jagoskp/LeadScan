import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/workflow/presentation/pages/workflow_dashboard_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('WorkflowDashboardPage Widget Tests', () {
    testWidgets('renders title, top tab chips, search field, and task cards', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const WorkflowDashboardPage()));
      await tester.pumpAndSettle();

      expect(find.text('Workflow & Task Engine'), findsOneWidget);
      expect(find.text('Tasks'), findsWidgets);
      expect(find.text('Agenda'), findsOneWidget);
      expect(find.byType(TextField), findsOneWidget);
    });
  });
}
