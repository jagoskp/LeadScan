import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/shared/widgets/lead_card_base.dart';
import 'package:leadscan_mobile/shared/widgets/sync_status_chip.dart';

void main() {
  group('LeadCardBase Widget Tests', () {
    testWidgets('renders lead name, title, company, confidence score and sync status', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: LeadCardBase(
              name: 'Sarah Connor',
              company: 'Cyberdyne Systems',
              title: 'VP of Technology',
              aiConfidenceScore: 0.95,
              syncStatus: SyncStatus.synced,
            ),
          ),
        ),
      );

      expect(find.text('Sarah Connor'), findsOneWidget);
      expect(find.text('VP of Technology • Cyberdyne Systems'), findsOneWidget);
      expect(find.text('AI 95% High'), findsOneWidget);
      expect(find.text('Synced'), findsOneWidget);
    });
  });
}
