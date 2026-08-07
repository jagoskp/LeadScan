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

import '../domain/usecases_test.dart';

void main() {
  late MockAuthRepository mockRepo;
  late AuthController controller;

  setUp(() {
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
  });
}
