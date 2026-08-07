import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/scanner/data/datasources/camera_datasource.dart';
import 'package:leadscan_mobile/features/scanner/data/datasources/gallery_datasource.dart';
import 'package:leadscan_mobile/features/scanner/data/repositories/scanner_repository_impl.dart';
import 'package:leadscan_mobile/features/scanner/domain/entities/camera_spec_entity.dart';

void main() {
  late ScannerRepositoryImpl repository;

  setUp(() {
    repository = ScannerRepositoryImpl(
      cameraDataSource: CameraDataSourceImpl(isMock: true),
      galleryDataSource: GalleryDataSourceImpl(),
    );
  });

  group('ScannerRepositoryImpl Unit Tests', () {
    test('checkPermission returns ScannerPermissionStatus.granted', () async {
      final result = await repository.checkPermission();
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (status) => expect(status, ScannerPermissionStatus.granted),
      );
    });

    test('requestPermission returns ScannerPermissionStatus.granted', () async {
      final result = await repository.requestPermission();
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (status) => expect(status, ScannerPermissionStatus.granted),
      );
    });

    test('captureCard returns valid ScanCaptureEntity', () async {
      final result = await repository.captureCard(flashMode: FlashModeOption.off);
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (capture) {
          expect(capture.id, isNotEmpty);
          expect(capture.path, contains('/mock/scans/'));
        },
      );
    });

    test('pickFromGallery returns valid ScanCaptureEntity', () async {
      final result = await repository.pickFromGallery();
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (capture) {
          expect(capture, isNotNull);
          expect(capture?.path, contains('/mock/gallery/'));
        },
      );
    });
  });
}
