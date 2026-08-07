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
import 'package:leadscan_mobile/features/auth/presentation/pages/register_page.dart';

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
        home: RegisterPage(),
      ),
    );
  }

  group('RegisterPage Widget Tests', () {
    testWidgets('renders all input fields and CTA button', (tester) async {
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      expect(find.text('Create Account'), findsNWidgets(2));
      expect(find.text('Full Name'), findsOneWidget);
      expect(find.text('Email address'), findsOneWidget);
      expect(find.text('Phone Number'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
      expect(find.text('Confirm Password'), findsOneWidget);
    });

    testWidgets('triggers field validation on submit empty', (tester) async {
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      final createAccountBtn = find.text('Create Account').last;
      await tester.ensureVisible(createAccountBtn);
      await tester.tap(createAccountBtn);
      await tester.pumpAndSettle();

      expect(find.text('Full name is required.'), findsOneWidget);
      expect(find.text('Email address is required.'), findsOneWidget);
    });
  });
}
