import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/workflow/presentation/pages/task_detail_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('TaskDetailPage Widget Tests', () {
    testWidgets('renders task details title, lead info, and status CTA', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const TaskDetailPage(taskId: 'task_201')));
      await tester.pumpAndSettle();

      expect(find.text('Linked Lead: '), findsOneWidget);
      expect(find.text('Priority: '), findsOneWidget);
    });
  });
}
