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
import 'package:leadscan_mobile/features/auth/presentation/pages/login_page.dart';

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
        home: LoginPage(),
      ),
    );
  }

  group('LoginPage Widget Tests', () {
    testWidgets('renders all essential UI elements matching Stitch design', (tester) async {
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      expect(find.text('Welcome back'), findsOneWidget);
      expect(find.text('Log in to LeadScan AI to continue.'), findsOneWidget);
      expect(find.text('Email address'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
      expect(find.text('Remember me'), findsOneWidget);
      expect(find.text('Forgot Password?'), findsOneWidget);
      expect(find.text('Google'), findsOneWidget);
      expect(find.text('Sign up'), findsOneWidget);
    });

    testWidgets('shows validation errors when submitting empty form', (tester) async {
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      final loginBtn = find.text('Log in');
      await tester.tap(loginBtn);
      await tester.pumpAndSettle();

      expect(find.text('Email address is required.'), findsOneWidget);
      expect(find.text('Password is required.'), findsOneWidget);
    });
  });
}
