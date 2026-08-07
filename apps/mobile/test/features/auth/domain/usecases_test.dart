import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/error/failures.dart';
import 'package:leadscan_mobile/features/auth/domain/entities/user_entity.dart';
import 'package:leadscan_mobile/features/auth/domain/repositories/auth_repository.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/login_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/register_usecase.dart';
import 'package:leadscan_mobile/features/auth/domain/usecases/send_otp_usecase.dart';

class MockAuthRepository implements AuthRepository {
  @override
  Future<Either<Failure, UserEntity>> login({
    required String email,
    required String password,
    bool rememberMe = false,
  }) async {
    if (email == 'error@leadscan.ai') {
      return const Left(ValidationFailure('Invalid credentials'));
    }
    return const Right(
      UserEntity(
        id: 'usr_1',
        email: 'user@leadscan.ai',
        name: 'Test User',
      ),
    );
  }

  @override
  Future<Either<Failure, UserEntity>> loginWithGoogle({
    required String idToken,
    String? email,
    String? name,
    String? photoUrl,
  }) async {
    return Right(
      UserEntity(
        id: 'usr_g1',
        email: email ?? 'google@leadscan.ai',
        name: name ?? 'Google Test User',
      ),
    );
  }

  @override
  Future<Either<Failure, UserEntity>> register({
    required String name,
    required String email,
    required String phone,
    required String password,
  }) async {
    return Right(
      UserEntity(
        id: 'usr_2',
        email: email,
        name: name,
        phone: phone,
      ),
    );
  }

  @override
  Future<Either<Failure, void>> sendOtp({required String email}) async {
    return const Right(null);
  }

  @override
  Future<Either<Failure, bool>> verifyOtp({required String email, required String otp}) async {
    return const Right(true);
  }

  @override
  Future<Either<Failure, void>> resetPassword({
    required String email,
    required String otp,
    required String newPassword,
  }) async {
    return const Right(null);
  }

  @override
  Future<Either<Failure, UserEntity>> loginWithBiometrics() async {
    return const Right(
      UserEntity(id: 'usr_1', email: 'user@leadscan.ai', name: 'Test User'),
    );
  }

  @override
  Future<Either<Failure, void>> setBiometricEnabled(bool enabled) async {
    return const Right(null);
  }

  @override
  Future<bool> isBiometricAvailable() async => true;

  @override
  Future<Either<Failure, UserEntity?>> getSession() async => const Right(null);

  @override
  Future<Either<Failure, void>> logout() async => const Right(null);
}

void main() {
  late MockAuthRepository mockRepository;
  late LoginUseCase loginUseCase;
  late RegisterUseCase registerUseCase;
  late SendOtpUseCase sendOtpUseCase;

  setUp(() {
    mockRepository = MockAuthRepository();
    loginUseCase = LoginUseCase(mockRepository);
    registerUseCase = RegisterUseCase(mockRepository);
    sendOtpUseCase = SendOtpUseCase(mockRepository);
  });

  group('UseCases Test Suite', () {
    test('LoginUseCase returns UserEntity on success', () async {
      final result = await loginUseCase(
        email: 'user@leadscan.ai',
        password: 'Password123!',
      );

      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (r) => expect(r.email, 'user@leadscan.ai'),
      );
    });

    test('LoginUseCase returns Failure on invalid email', () async {
      final result = await loginUseCase(
        email: 'error@leadscan.ai',
        password: 'Password123!',
      );

      expect(result.isLeft(), isTrue);
    });

    test('RegisterUseCase returns newly registered UserEntity', () async {
      final result = await registerUseCase(
        name: 'Jane Doe',
        email: 'jane@leadscan.ai',
        phone: '+15550192834',
        password: 'Password123!',
      );

      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (r) => expect(r.name, 'Jane Doe'),
      );
    });

    test('SendOtpUseCase returns void Right on success', () async {
      final result = await sendOtpUseCase(email: 'user@leadscan.ai');
      expect(result.isRight(), isTrue);
    });
  });
}
