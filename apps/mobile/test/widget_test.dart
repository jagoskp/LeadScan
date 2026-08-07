import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/config/env_config.dart';
import 'package:leadscan_mobile/main.dart';

void main() {
  testWidgets('LeadScanApp foundation smoke test', (WidgetTester tester) async {
    EnvConfig.init(Environment.dev);
    expect(EnvConfig.current.environment, Environment.dev);
    expect(EnvConfig.current.enableLogging, true);

    await tester.pumpWidget(
      const ProviderScope(
        child: LeadScanApp(),
      ),
    );
    expect(find.byType(LeadScanApp), findsOneWidget);
  });
}
