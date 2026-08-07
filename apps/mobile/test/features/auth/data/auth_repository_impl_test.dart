import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/network/network_info.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/biometric_auth_service.dart';
import 'package:leadscan_mobile/features/auth/data/models/auth_tokens_model.dart';
import 'package:leadscan_mobile/features/auth/data/models/user_model.dart';
import 'package:leadscan_mobile/features/auth/data/repositories/auth_repository_impl.dart';

class MockNetworkInfo implements NetworkInfo {
  final bool connected;
  MockNetworkInfo({this.connected = true});

  @override
  Future<bool> get isConnected async => connected;
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
  });
}
