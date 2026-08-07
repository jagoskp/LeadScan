import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/di/service_locator.dart';
import 'package:leadscan_mobile/core/network/network_info.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/biometric_auth_service.dart';
import 'package:leadscan_mobile/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:leadscan_mobile/features/auth/domain/repositories/auth_repository.dart';
import 'package:leadscan_mobile/features/auth/presentation/pages/otp_verification_page.dart';

import '../../data/auth_repository_impl_test.dart';

void main() {
  setUp(() async {
    await sl.reset();
    sl.registerLazySingleton<AuthLocalDataSource>(() => MockAuthLocalDataSource());
    sl.registerLazySingleton<AuthRemoteDataSource>(() => MockAuthRemoteDataSourceImpl());
    sl.registerLazySingleton<BiometricAuthService>(() => MockBiometricAuthService());
    sl.registerLazySingleton<NetworkInfo>(() => MockNetworkInfo());
    sl.registerLazySingleton<AuthRepository>(
      () => AuthRepositoryImpl(
        remoteDataSource: sl<AuthRemoteDataSource>(),
        localDataSource: sl<AuthLocalDataSource>(),
        biometricService: sl<BiometricAuthService>(),
        networkInfo: sl<NetworkInfo>(),
      ),
    );
  });

  Widget createWidgetUnderTest() {
    return const ProviderScope(
      child: MaterialApp(
        home: OtpVerificationPage(email: 'user@leadscan.ai'),
      ),
    );
  }

  group('OtpVerificationPage Widget Tests', () {
    testWidgets('renders title, email subtitle and verify button', (tester) async {
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      expect(find.text('Enter Verification Code'), findsOneWidget);
      expect(find.textContaining('user@leadscan.ai'), findsOneWidget);
      expect(find.text('Verify Code'), findsOneWidget);
    });
  });
}
