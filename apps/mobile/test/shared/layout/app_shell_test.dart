import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/shared/layout/app_navigation.dart';
import 'package:leadscan_mobile/shared/layout/app_responsive_layout.dart';

void main() {
  group('AppShell & Responsive Layout Suite', () {
    testWidgets('AppBottomNavigationBar renders 5 destinations', (tester) async {
      int selectedIndex = 0;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            bottomNavigationBar: AppBottomNavigationBar(
              selectedIndex: selectedIndex,
              onDestinationSelected: (idx) => selectedIndex = idx,
              destinations: const [
                AppNavigationDestination(
                  label: 'Dashboard',
                  icon: Icons.dashboard_outlined,
                  selectedIcon: Icons.dashboard_rounded,
                  routePath: '/dashboard',
                ),
                AppNavigationDestination(
                  label: 'Scanner',
                  icon: Icons.qr_code_scanner_outlined,
                  selectedIcon: Icons.qr_code_scanner_rounded,
                  routePath: '/scanner',
                ),
                AppNavigationDestination(
                  label: 'Leads',
                  icon: Icons.people_outline_rounded,
                  selectedIcon: Icons.people_rounded,
                  routePath: '/leads',
                ),
                AppNavigationDestination(
                  label: 'Workflow',
                  icon: Icons.account_tree_outlined,
                  selectedIcon: Icons.account_tree_rounded,
                  routePath: '/workflow',
                ),
                AppNavigationDestination(
                  label: 'Profile',
                  icon: Icons.person_outline_rounded,
                  selectedIcon: Icons.person_rounded,
                  routePath: '/profile',
                ),
              ],
            ),
          ),
        ),
      );

      expect(find.text('Dashboard'), findsOneWidget);
      expect(find.text('Scanner'), findsOneWidget);
      expect(find.text('Leads'), findsOneWidget);
      expect(find.text('Workflow'), findsOneWidget);
      expect(find.text('Profile'), findsOneWidget);
    });

    testWidgets('AppResponsiveLayout renders mobile view on small screens', (tester) async {
      tester.view.physicalSize = const Size(400, 800);
      tester.view.devicePixelRatio = 1.0;

      await tester.pumpWidget(
        const MaterialApp(
          home: AppResponsiveLayout(
            mobile: Text('Mobile Layout View'),
            tablet: Text('Tablet Layout View'),
          ),
        ),
      );

      expect(find.text('Mobile Layout View'), findsOneWidget);
      expect(find.text('Tablet Layout View'), findsNothing);

      addTearDown(tester.view.resetPhysicalSize);
    });

    testWidgets('AppResponsiveLayout renders tablet view on large screens', (tester) async {
      tester.view.physicalSize = const Size(800, 1000);
      tester.view.devicePixelRatio = 1.0;

      await tester.pumpWidget(
        const MaterialApp(
          home: AppResponsiveLayout(
            mobile: Text('Mobile Layout View'),
            tablet: Text('Tablet Layout View'),
          ),
        ),
      );

      expect(find.text('Tablet Layout View'), findsOneWidget);
      expect(find.text('Mobile Layout View'), findsNothing);

      addTearDown(tester.view.resetPhysicalSize);
    });
  });
}
