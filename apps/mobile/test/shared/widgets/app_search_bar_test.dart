import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/shared/widgets/app_search_bar.dart';

void main() {
  group('AppSearchField Component Suite', () {
    testWidgets('AppSearchField renders hint text and filter button', (tester) async {
      bool filterTapped = false;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppSearchField(
              hint: 'Search leads...',
              onFilterPressed: () => filterTapped = true,
            ),
          ),
        ),
      );

      expect(find.text('Search leads...'), findsOneWidget);
      expect(find.byIcon(Icons.tune_rounded), findsOneWidget);

      await tester.tap(find.byIcon(Icons.tune_rounded));
      expect(filterTapped, isTrue);
    });
  });
}
