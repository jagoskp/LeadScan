import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/scanner/data/datasources/camera_datasource.dart';
import 'package:leadscan_mobile/features/scanner/data/datasources/gallery_datasource.dart';
import 'package:leadscan_mobile/features/scanner/data/repositories/scanner_repository_impl.dart';
import 'package:leadscan_mobile/features/scanner/domain/entities/camera_spec_entity.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/capture_card_usecase.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/check_camera_permission_usecase.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/request_camera_permission_usecase.dart';
import 'package:leadscan_mobile/features/scanner/presentation/controllers/scanner_controller.dart';

void main() {
  late ScannerController controller;

  setUp(() {
    final repo = ScannerRepositoryImpl(
      cameraDataSource: CameraDataSourceImpl(isMock: true),
      galleryDataSource: GalleryDataSourceImpl(),
    );
    controller = ScannerController(
      checkPermissionUseCase: CheckCameraPermissionUseCase(repo),
      requestPermissionUseCase: RequestCameraPermissionUseCase(repo),
      captureCardUseCase: CaptureCardUseCase(repo),
    );
  });

  group('ScannerController Tests', () {
    test('initial state checks permission and initializes', () async {
      await Future.delayed(const Duration(milliseconds: 150));
      expect(controller.state.permissionStatus, ScannerPermissionStatus.granted);
      expect(controller.state.isCameraInitialized, isTrue);
    });

    test('toggleFlash cycles off -> auto -> torch -> off', () {
      expect(controller.state.flashMode, FlashModeOption.off);
      controller.toggleFlash();
      expect(controller.state.flashMode, FlashModeOption.auto);
      controller.toggleFlash();
      expect(controller.state.flashMode, FlashModeOption.torch);
      controller.toggleFlash();
      expect(controller.state.flashMode, FlashModeOption.off);
    });

    test('switchCamera toggles front facing state', () {
      expect(controller.state.isFrontFacing, isFalse);
      controller.switchCamera();
      expect(controller.state.isFrontFacing, isTrue);
    });

    test('setScannerMode changes to batchScan', () {
      controller.setScannerMode(ScannerMode.batchScan);
      expect(controller.state.scannerMode, ScannerMode.batchScan);
    });

    test('captureCard appends capture to list', () async {
      await controller.captureCard();
      expect(controller.state.capturedCards.length, 1);
    });
  });
}
