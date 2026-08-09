import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/dashboard/data/repositories/dashboard_repository_impl.dart';
import 'package:leadscan_mobile/features/dashboard/domain/usecases/get_dashboard_summary_usecase.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/controllers/dashboard_controller.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/controllers/dashboard_state.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({'auth_user_name': 'Test User'});

  group('DashboardController Unit Tests', () {
    test('initial state loads summary successfully', () async {
      final repository = DashboardRepositoryImpl();
      final useCase = GetDashboardSummaryUseCase(repository);
      final controller = DashboardController(useCase);

      await Future.delayed(const Duration(milliseconds: 500));

      expect(controller.state.status, DashboardStatus.success);
      expect(controller.state.summary, isNotNull);
      expect(controller.state.summary?.userName, 'Test User');
    });

    test('refresh reloads data into state', () async {
      final repository = DashboardRepositoryImpl();
      final useCase = GetDashboardSummaryUseCase(repository);
      final controller = DashboardController(useCase);

      await Future.delayed(const Duration(milliseconds: 500));

      await controller.refresh();
      expect(controller.state.status, DashboardStatus.success);
      expect(controller.state.isRefreshing, isFalse);
    });
  });
}
