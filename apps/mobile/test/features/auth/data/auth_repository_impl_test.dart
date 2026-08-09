import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/network/network_info.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/biometric_auth_service.dart';
import 'package:leadscan_mobile/features/auth/data/models/auth_tokens_model.dart';
import 'package:leadscan_mobile/features/auth/data/models/user_model.dart';
import 'package:leadscan_mobile/features/auth/data/repositories/auth_repository_impl.dart';

import 'package:leadscan_mobile/features/auth/data/dtos/auth_response_dto.dart';
import 'package:leadscan_mobile/features/auth/data/dtos/auth_tokens_dto.dart';
import 'package:leadscan_mobile/features/auth/data/dtos/login_request_dto.dart';
import 'package:leadscan_mobile/features/auth/data/dtos/register_request_dto.dart';
import 'package:leadscan_mobile/features/auth/data/dtos/reset_password_request_dto.dart';

class MockNetworkInfo implements NetworkInfo {
  final bool connected;
  MockNetworkInfo({this.connected = true});

  @override
  Future<bool> get isConnected async => connected;
}

class MockAuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  @override
  Future<AuthResponseDto> googleLogin({
    required String idToken,
    String? email,
    String? name,
    String? photoUrl,
  }) async {
    return AuthResponseDto(
      user: UserModel(
        id: 'usr_123',
        email: email ?? 'user@leadscan.ai',
        name: name ?? 'LeadScan User',
        isEmailVerified: true,
      ),
      tokens: const AuthTokensDto(
        accessToken: 'access_123',
        refreshToken: 'refresh_123',
      ),
    );
  }

  @override
  Future<AuthResponseDto> login(LoginRequestDto request) async {
    return AuthResponseDto(
      user: UserModel(
        id: 'usr_123',
        email: request.email,
        name: request.email.split('@').first,
        isEmailVerified: true,
      ),
      tokens: const AuthTokensDto(
        accessToken: 'access_123',
        refreshToken: 'refresh_123',
      ),
    );
  }

  @override
  Future<AuthResponseDto> register(RegisterRequestDto request) async {
    return AuthResponseDto(
      user: UserModel(
        id: 'usr_456',
        email: request.email,
        name: request.name,
        isEmailVerified: true,
      ),
      tokens: const AuthTokensDto(
        accessToken: 'access_456',
        refreshToken: 'refresh_456',
      ),
    );
  }

  @override
  Future<void> sendOtp(String email) async {}

  @override
  Future<bool> verifyOtp(String email, String otp) async => true;

  @override
  Future<void> resetPassword(ResetPasswordRequestDto request) async {}

  @override
  Future<void> logout() async {}
}

class MockAuthLocalDataSource implements AuthLocalDataSource {
  UserModel? _storedUser;
  AuthTokensModel? _storedTokens;
  bool _biometricEnabled = false;

  @override
  Future<void> clearAll() async {
    _storedUser = null;
    _storedTokens = null;
  }

  @override
  Future<void> clearTokens() async => _storedTokens = null;

  @override
  Future<void> clearUser() async => _storedUser = null;

  @override
  Future<AuthTokensModel?> getTokens() async => _storedTokens;

  @override
  Future<UserModel?> getUser() async => _storedUser;

  @override
  Future<bool> isBiometricEnabled() async => _biometricEnabled;

  @override
  Future<void> saveTokens(AuthTokensModel tokens) async => _storedTokens = tokens;

  @override
  Future<void> saveUser(UserModel user) async => _storedUser = user;

  @override
  Future<void> setBiometricEnabled(bool enabled) async => _biometricEnabled = enabled;

  @override
  Future<void> setPin(String pin) async {}

  @override
  Future<bool> verifyPin(String pin) async => true;

  @override
  Future<bool> hasPin() async => true;
}

class MockBiometricAuthService implements BiometricAuthService {
  @override
  Future<bool> authenticate({String reason = ''}) async => true;

  @override
  Future<bool> isBiometricAvailable() async => true;
}

void main() {
  late AuthRepositoryImpl repository;
  late MockAuthRemoteDataSourceImpl remoteDataSource;
  late MockAuthLocalDataSource localDataSource;
  late MockBiometricAuthService biometricService;
  late MockNetworkInfo networkInfo;

  setUp(() {
    remoteDataSource = MockAuthRemoteDataSourceImpl();
    localDataSource = MockAuthLocalDataSource();
    biometricService = MockBiometricAuthService();
    networkInfo = MockNetworkInfo(connected: true);

    repository = AuthRepositoryImpl(
      remoteDataSource: remoteDataSource,
      localDataSource: localDataSource,
      biometricService: biometricService,
      networkInfo: networkInfo,
    );
  });

  group('AuthRepositoryImpl', () {
    test('login succeeds and persists user/tokens when rememberMe is true', () async {
      final result = await repository.login(
        email: 'user@leadscan.ai',
        password: 'Password123!',
        rememberMe: true,
      );

      expect(result.isRight(), isTrue);
      final savedUser = await localDataSource.getUser();
      expect(savedUser, isNotNull);
      expect(savedUser?.email, 'user@leadscan.ai');
    });

    test('login fails when disconnected from network', () async {
      final offlineRepo = AuthRepositoryImpl(
        remoteDataSource: remoteDataSource,
        localDataSource: localDataSource,
        biometricService: biometricService,
        networkInfo: MockNetworkInfo(connected: false),
      );

      final result = await offlineRepo.login(
        email: 'user@leadscan.ai',
        password: 'Password123!',
      );

      expect(result.isLeft(), isTrue);
    });

    test('register succeeds and saves session locally', () async {
      final result = await repository.register(
        name: 'New Enterprise User',
        email: 'newuser@leadscan.ai',
        phone: '+15551234567',
        password: 'Password123!',
      );

      expect(result.isRight(), isTrue);
      final user = await localDataSource.getUser();
      expect(user?.name, 'New Enterprise User');
    });

    test('logout clears local tokens and user session', () async {
      await localDataSource.saveUser(const UserModel(id: 'usr_1', email: 'accountA@gmail.com', name: 'User A'));
      await localDataSource.saveTokens(const AuthTokensModel(accessToken: 'tokenA', refreshToken: 'refA'));

      final logoutResult = await repository.logout();
      expect(logoutResult.isRight(), isTrue);

      final user = await localDataSource.getUser();
      final tokens = await localDataSource.getTokens();
      expect(user, isNull);
      expect(tokens, isNull);
    });

    test('Google login Account A followed by logout and Google login Account B succeeds', () async {
      final loginA = await repository.loginWithGoogle(idToken: 'tokenA', email: 'accountA@gmail.com', name: 'Account A');
      expect(loginA.isRight(), isTrue);
      loginA.fold((l) => fail('A failed'), (userA) => expect(userA.email, 'accountA@gmail.com'));

      final logoutResult = await repository.logout();
      expect(logoutResult.isRight(), isTrue);

      final loginB = await repository.loginWithGoogle(idToken: 'tokenB', email: 'accountB@gmail.com', name: 'Account B');
      expect(loginB.isRight(), isTrue);
      loginB.fold((l) => fail('B failed'), (userB) => expect(userB.email, 'accountB@gmail.com'));
    });
  });
}
