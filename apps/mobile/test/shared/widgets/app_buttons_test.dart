import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/shared/widgets/app_buttons.dart';

void main() {
  group('AppButtons Component Suite', () {
    testWidgets('AppFilledButton renders text and triggers callback', (tester) async {
      bool tapped = false;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppFilledButton(
              text: 'Submit Lead',
              onPressed: () => tapped = true,
            ),
          ),
        ),
      );

      expect(find.text('Submit Lead'), findsOneWidget);
      await tester.tap(find.text('Submit Lead'));
      expect(tapped, isTrue);
    });

    testWidgets('AppFilledButton renders progress indicator when isLoading is true', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AppFilledButton(
              text: 'Loading...',
              isLoading: true,
            ),
          ),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('AppTonalButton renders correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppTonalButton(
              text: 'Secondary Action',
              onPressed: () {},
            ),
          ),
        ),
      );

      expect(find.text('Secondary Action'), findsOneWidget);
    });

    testWidgets('AppOutlinedButton renders correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppOutlinedButton(
              text: 'Outlined Action',
              onPressed: () {},
            ),
          ),
        ),
      );

      expect(find.text('Outlined Action'), findsOneWidget);
    });

    testWidgets('AppFab renders floating action button', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            floatingActionButton: AppFab(
              icon: Icons.add_rounded,
              label: 'Add Lead',
              onPressed: () {},
            ),
          ),
        ),
      );

      expect(find.byType(FloatingActionButton), findsOneWidget);
    });
  });
}
