import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/image_processor.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/ocr_datasource.dart';
import 'package:leadscan_mobile/features/ocr/data/repositories/ocr_repository_impl.dart';
import 'package:leadscan_mobile/features/ocr/domain/entities/ocr_result_entity.dart';
import 'package:leadscan_mobile/features/ocr/domain/strategies/ocr_engine_strategy.dart';
import 'package:leadscan_mobile/features/ocr/domain/usecases/process_image_ocr_usecase.dart';
import 'package:leadscan_mobile/features/ocr/presentation/controllers/ocr_processing_controller.dart';

void main() {
  late OcrProcessingController controller;

  setUp(() {
    final repo = OcrRepositoryImpl(
      imageProcessor: ImageProcessor(),
      ocrDataSource: OcrDataSourceImpl(),
    );
    controller = OcrProcessingController(
      processImageOcrUseCase: ProcessImageOcrUseCase(repo),
    );
  });

  group('OcrProcessingController Unit Tests', () {
    test('initial state is idle', () {
      expect(controller.state.stage, OcrProcessingStage.idle);
      expect(controller.state.progress, 0.0);
    });

    test('startProcessing advances state to completed and sets extractedLead', () async {
      await controller.startProcessing('/valid/card.jpg');
      expect(controller.state.stage, OcrProcessingStage.completed);
      expect(controller.state.progress, 1.0);
      expect(controller.state.extractedLead, isNotNull);
      expect(controller.state.extractedLead?.fullName.value, 'Alex Morgan');
    });

    test('cancelProcessing resets state and sets isCancelled flag', () {
      controller.cancelProcessing();
      expect(controller.state.isCancelled, isTrue);
      expect(controller.state.stage, OcrProcessingStage.idle);
    });

    test('setOcrProvider updates active provider in state', () {
      controller.setOcrProvider(OcrProviderType.tesseract);
      expect(controller.state.provider, OcrProviderType.tesseract);
    });
  });
}
