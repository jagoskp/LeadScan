import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/shared/widgets/metric_card.dart';

void main() {
  group('MetricCard Widget Tests', () {
    testWidgets('renders KPI title, value and trend indicator', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: MetricCard(
              title: 'Total Scanned Leads',
              value: '1,248',
              trendLabel: '+14.2%',
              isTrendPositive: true,
              icon: Icons.people_alt_rounded,
            ),
          ),
        ),
      );

      expect(find.text('1,248'), findsOneWidget);
      expect(find.text('Total Scanned Leads'), findsOneWidget);
      expect(find.text('+14.2%'), findsOneWidget);
      expect(find.byIcon(Icons.trending_up_rounded), findsOneWidget);
    });
  });
}
