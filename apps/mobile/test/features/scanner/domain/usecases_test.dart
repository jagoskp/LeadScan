import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/scanner/data/datasources/camera_datasource.dart';
import 'package:leadscan_mobile/features/scanner/data/datasources/gallery_datasource.dart';
import 'package:leadscan_mobile/features/scanner/data/repositories/scanner_repository_impl.dart';
import 'package:leadscan_mobile/features/scanner/domain/entities/camera_spec_entity.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/capture_card_usecase.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/check_camera_permission_usecase.dart';
import 'package:leadscan_mobile/features/scanner/domain/usecases/request_camera_permission_usecase.dart';

void main() {
  late ScannerRepositoryImpl repository;
  late CheckCameraPermissionUseCase checkPermissionUseCase;
  late RequestCameraPermissionUseCase requestPermissionUseCase;
  late CaptureCardUseCase captureCardUseCase;

  setUp(() {
    repository = ScannerRepositoryImpl(
      cameraDataSource: CameraDataSourceImpl(isMock: true),
      galleryDataSource: GalleryDataSourceImpl(),
    );
    checkPermissionUseCase = CheckCameraPermissionUseCase(repository);
    requestPermissionUseCase = RequestCameraPermissionUseCase(repository);
    captureCardUseCase = CaptureCardUseCase(repository);
  });

  group('Scanner UseCases Tests', () {
    test('CheckCameraPermissionUseCase returns status', () async {
      final result = await checkPermissionUseCase();
      expect(result.isRight(), isTrue);
    });

    test('RequestCameraPermissionUseCase returns status', () async {
      final result = await requestPermissionUseCase();
      expect(result.isRight(), isTrue);
    });

    test('CaptureCardUseCase captures card', () async {
      final result = await captureCardUseCase(flashMode: FlashModeOption.off);
      expect(result.isRight(), isTrue);
    });
  });
}
