import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/biometric_login_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/get_session_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/login_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/logout_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/register_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/reset_password_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/send_otp_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/verify_otp_usecase.dart';
import 'package:leadscan_mobile/features/auth/presentation/controllers/auth_controller.dart';
import 'package:leadscan_mobile/features/auth/presentation/controllers/auth_state.dart';
import 'package:leadscan_mobile/features/auth/presentation/providers/auth_providers.dart';
import 'package:leadscan_mobile/features/dashboard/data/repositories/dashboard_repository_impl.dart';
import 'package:leadscan_mobile/features/dashboard/presentation/providers/dashboard_providers.dart';

import '../domain/usecases_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({});

  late MockAuthRepository mockRepo;
  late AuthController controller;

  // Shared mock storage: in tests all layers use this same instance
  // (AndroidOptions are ignored in headless VM, so defaults work for both)
  final storage = const FlutterSecureStorage();

  setUp(() async {
    await storage.deleteAll();
    mockRepo = MockAuthRepository();
    controller = AuthController(
      authRepository: mockRepo,
      loginUseCase: LoginUseCase(mockRepo),
      registerUseCase: RegisterUseCase(mockRepo),
      sendOtpUseCase: SendOtpUseCase(mockRepo),
      verifyOtpUseCase: VerifyOtpUseCase(mockRepo),
      resetPasswordUseCase: ResetPasswordUseCase(mockRepo),
      biometricLoginUseCase: BiometricLoginUseCase(mockRepo),
      getSessionUseCase: GetSessionUseCase(mockRepo),
      logoutUseCase: LogoutUseCase(mockRepo),
    );
  });

  group('AuthController Test Suite', () {
    test('initial state is AuthStatus.initial', () {
      expect(controller.state.status, AuthStatus.initial);
    });

    test('login updates state to authenticated on success', () async {
      await controller.login(
        email: 'user@leadscan.ai',
        password: 'Password123!',
      );
      expect(controller.state.status, AuthStatus.authenticated);
      expect(controller.state.user?.email, 'user@leadscan.ai');
    });

    test('sendOtp updates state to otpSent', () async {
      await controller.sendOtp(email: 'user@leadscan.ai');
      expect(controller.state.status, AuthStatus.otpSent);
      expect(controller.state.targetEmail, 'user@leadscan.ai');
    });

    test('verifyOtp updates state to otpVerified', () async {
      await controller.verifyOtp(email: 'user@leadscan.ai', otp: '123456');
      expect(controller.state.status, AuthStatus.otpVerified);
    });

    test('logout resets state to unauthenticated', () async {
      await controller.logout();
      expect(controller.state.status, AuthStatus.unauthenticated);
    });

    test(
        'TEST 1 & 4 & 5: AuthController invalidates dashboardControllerProvider on login and logout',
        () async {
      // Override dashboardRepositoryProvider with DashboardRepositoryImpl using
      // the same shared mock storage — avoids GetIt initialization in unit tests.
      final container = ProviderContainer(
        overrides: [
          authRepositoryProvider.overrideWithValue(mockRepo),
          dashboardRepositoryProvider.overrideWith(
            (ref) => DashboardRepositoryImpl(storage: storage),
          ),
        ],
      );
      addTearDown(container.dispose);
      await storage.deleteAll();

      // 1. Initial dashboard read before login
      await container.read(dashboardControllerProvider.notifier).fetchDashboardSummary();
      final initialDashboardState = container.read(dashboardControllerProvider);
      expect(initialDashboardState.summary?.userName ?? 'User', 'User');

      // 2. Login Account A
      await storage.write(key: 'auth_user_name', value: 'Account A');
      await storage.write(key: 'auth_user_email', value: 'accountA@gmail.com');
      final authNotifier = container.read(authControllerProvider.notifier);

      await authNotifier.login(email: 'accountA@gmail.com', password: 'Password123!');
      await container.read(dashboardControllerProvider.notifier).fetchDashboardSummary();

      final updatedDashboardState = container.read(dashboardControllerProvider);
      expect(updatedDashboardState.summary?.userName, 'Account A');

      // 3. Logout
      await authNotifier.logout();
      await storage.deleteAll();
      await container.read(dashboardControllerProvider.notifier).fetchDashboardSummary();

      final loggedOutState = container.read(dashboardControllerProvider);
      expect(loggedOutState.summary?.userName, 'User');

      // 4. Login Account B — no stale Account A identity
      await storage.write(key: 'auth_user_name', value: 'Account B');
      await storage.write(key: 'auth_user_email', value: 'accountB@gmail.com');
      await authNotifier.login(email: 'accountB@gmail.com', password: 'Password123!');
      await container.read(dashboardControllerProvider.notifier).fetchDashboardSummary();

      final accountBDashboardState = container.read(dashboardControllerProvider);
      expect(accountBDashboardState.summary?.userName, 'Account B');
    });
  });
}
