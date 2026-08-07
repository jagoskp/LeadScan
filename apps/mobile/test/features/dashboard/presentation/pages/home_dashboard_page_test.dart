import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/pages/home_dashboard_page.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  GoogleFonts.config.allowRuntimeFetching = false;

  group('HomeDashboardPage Widget Tests', () {
    testWidgets('renders top bar, KPI cards, quick actions and lead cards', (tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: HomeDashboardPage(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      expect(find.text('Good morning 👋'), findsOneWidget);
      expect(find.text('Alex Morgan'), findsOneWidget);
      expect(find.text('Total Leads'), findsOneWidget);
      expect(find.text("Today's Leads"), findsOneWidget);
      expect(find.text('Pending Follow-ups'), findsOneWidget);
      expect(find.text('Quick Actions'), findsOneWidget);
      expect(find.text('Scan Business Card'), findsOneWidget);
      expect(find.text('Recent Lead Captures'), findsOneWidget);
      expect(find.text('Sarah Connor'), findsOneWidget);
    });
  });
}
