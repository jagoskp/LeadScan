import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/shared/widgets/ai_confidence_chip.dart';
import 'package:leadscan_mobile/shared/widgets/app_chips.dart';
import 'package:leadscan_mobile/shared/widgets/sync_status_chip.dart';

void main() {
  group('App Chips & Status Indicators Suite', () {
    testWidgets('AppChip renders label', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppChip(
              label: 'Filter Tag',
              onPressed: () {},
            ),
          ),
        ),
      );

      expect(find.text('Filter Tag'), findsOneWidget);
    });

    testWidgets('AiConfidenceChip displays High confidence score text', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AiConfidenceChip(score: 0.98),
          ),
        ),
      );

      expect(find.text('AI 98% High'), findsOneWidget);
    });

    testWidgets('SyncStatusChip displays Synced status', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: SyncStatusChip(status: SyncStatus.synced),
          ),
        ),
      );

      expect(find.text('Synced'), findsOneWidget);
    });
  });
}
