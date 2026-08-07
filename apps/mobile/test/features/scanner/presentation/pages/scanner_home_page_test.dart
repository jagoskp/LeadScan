import 'package:dartz/dartz.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/error/failures.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/scanner/domain/entities/camera_spec_entity.dart';
import 'package:leadscan_mobile/features/scanner/domain/repositories/scanner_repository.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/capture_card_usecase.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/check_camera_permission_usecase.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/request_camera_permission_usecase.dart';
import 'package:leadscan_mobile/features/scanner/presentation/controllers/scanner_controller.dart';
import 'package:leadscan_mobile/features/scanner/presentation/pages/scanner_home_page.dart';
import 'package:leadscan_mobile/features/scanner/presentation/providers/scanner_providers.dart';

class FakeScannerRepository implements ScannerRepository {
  final ScannerPermissionStatus permissionStatus;

  FakeScannerRepository({this.permissionStatus = ScannerPermissionStatus.granted});

  @override
  Future<Either<Failure, ScannerPermissionStatus>> checkPermission() async {
    return Right(permissionStatus);
  }

  @override
  Future<Either<Failure, ScannerPermissionStatus>> requestPermission() async {
    return Right(permissionStatus);
  }

  @override
  Future<Either<Failure, ScanCaptureEntity>> captureCard({
    required FlashModeOption flashMode,
  }) async {
    return Right(ScanCaptureEntity(
      id: '1',
      path: '/test/path.jpg',
      timestamp: DateTime.now(),
      width: 1920,
      height: 1080,
    ));
  }

  @override
  Future<Either<Failure, ScanCaptureEntity?>> pickFromGallery() async {
    return const Right(null);
  }
}

void main() {
  Widget buildTestableWidget({ScannerPermissionStatus status = ScannerPermissionStatus.granted}) {
    final fakeRepo = FakeScannerRepository(permissionStatus: status);
    final checkPermission = CheckCameraPermissionUseCase(fakeRepo);
    final requestPermission = RequestCameraPermissionUseCase(fakeRepo);
    final captureCard = CaptureCardUseCase(fakeRepo);

    return ProviderScope(
      overrides: [
        scannerControllerProvider.overrideWith(
          (ref) => ScannerController(
            checkPermissionUseCase: checkPermission,
            requestPermissionUseCase: requestPermission,
            captureCardUseCase: captureCard,
          ),
        ),
      ],
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: const ScannerHomePage(),
      ),
    );
  }

  group('ScannerHomePage Widget Tests', () {
    testWidgets('renders camera scanner UI when permission is granted', (tester) async {
      await tester.pumpWidget(buildTestableWidget(status: ScannerPermissionStatus.granted));
      await tester.pump(const Duration(milliseconds: 300));

      expect(find.text('Align business card inside frame'), findsOneWidget);
      expect(find.text('Single Card'), findsOneWidget);
      expect(find.text('Batch Scan'), findsOneWidget);
      expect(find.byIcon(Icons.camera_rounded), findsOneWidget);
    });

    testWidgets('renders permission request screen when permission is denied', (tester) async {
      await tester.pumpWidget(buildTestableWidget(status: ScannerPermissionStatus.denied));
      await tester.pump(const Duration(milliseconds: 300));

      expect(find.text('Camera Access Required'), findsOneWidget);
      expect(find.text('Grant Camera Access'), findsOneWidget);
    });
  });
}
