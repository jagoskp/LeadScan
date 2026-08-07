import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/image_processor.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/ocr_datasource.dart';
import 'package:leadscan_mobile/features/ocr/data/repositories/ocr_repository_impl.dart';
import 'package:leadscan_mobile/features/ocr/domain/entities/ocr_result_entity.dart';
import 'package:leadscan_mobile/features/ocr/domain/usecases/process_image_ocr_usecase.dart';

void main() {
  late ProcessImageOcrUseCase useCase;

  setUp(() {
    final repo = OcrRepositoryImpl(
      imageProcessor: ImageProcessor(),
      ocrDataSource: OcrDataSourceImpl(),
    );
    useCase = ProcessImageOcrUseCase(repo);
  });

  group('ProcessImageOcrUseCase Pipeline Unit Tests', () {
    test('executes multi-stage pipeline and reports progress', () async {
      final progressStages = <OcrProcessingStage>[];

      final result = await useCase(
        imagePath: '/valid/business_card.jpg',
        onProgress: (stage, progress) {
          progressStages.add(stage);
        },
      );

      expect(result.isRight(), isTrue);
      expect(progressStages, contains(OcrProcessingStage.validation));
      expect(progressStages, contains(OcrProcessingStage.preprocessing));
      expect(progressStages, contains(OcrProcessingStage.ocrScanning));
      expect(progressStages, contains(OcrProcessingStage.aiUnderstanding));
      expect(progressStages, contains(OcrProcessingStage.completed));
    });
  });
}
