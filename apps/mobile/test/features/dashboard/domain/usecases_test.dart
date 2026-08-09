import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/dashboard/data/repositories/dashboard_repository_impl.dart';
import 'package:leadscan_mobile/features/dashboard/domain/usecases/get_dashboard_summary_usecase.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({});

  group('GetDashboardSummaryUseCase Unit Tests', () {
    test('call delegates to DashboardRepository and returns data', () async {
      final repository = DashboardRepositoryImpl();
      final useCase = GetDashboardSummaryUseCase(repository);

      final result = await useCase();
      expect(result.isRight(), isTrue);
    });
  });
}
