import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/shared/widgets/app_cards.dart';

void main() {
  group('AppCard Component Suite', () {
    testWidgets('AppCard renders child content and responds to tap', (tester) async {
      bool tapped = false;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppCard(
              onTap: () => tapped = true,
              child: const Text('Card Body Content'),
            ),
          ),
        ),
      );

      expect(find.text('Card Body Content'), findsOneWidget);
      await tester.tap(find.text('Card Body Content'));
      expect(tapped, isTrue);
    });
  });
}
