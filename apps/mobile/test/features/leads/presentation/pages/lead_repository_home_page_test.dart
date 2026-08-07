import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/leads/presentation/pages/lead_repository_home_page.dart';

void main() {
  Widget buildTestableWidget(Widget child) {
    return ProviderScope(
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: child,
      ),
    );
  }

  group('LeadRepositoryHomePage Widget Tests', () {
    testWidgets('renders app bar title, search bar, and lead card items', (tester) async {
      await tester.pumpWidget(buildTestableWidget(const LeadRepositoryHomePage()));
      await tester.pumpAndSettle();

      expect(find.text('Lead Repository'), findsOneWidget);
      expect(find.byType(TextField), findsOneWidget);
      expect(find.text('Alex Morgan'), findsOneWidget);
    });
  });
}
