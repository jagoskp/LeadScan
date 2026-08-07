import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/image_processor.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/ocr_datasource.dart';
import 'package:leadscan_mobile/features/ocr/data/repositories/ocr_repository_impl.dart';
import 'package:leadscan_mobile/features/ocr/domain/entities/ocr_result_entity.dart';
import 'package:leadscan_mobile/features/ocr/domain/strategies/ocr_engine_strategy.dart';

void main() {
  late OcrRepositoryImpl repository;

  setUp(() {
    repository = OcrRepositoryImpl(
      imageProcessor: ImageProcessor(),
      ocrDataSource: OcrDataSourceImpl(),
    );
  });

  group('OcrRepositoryImpl Strategy & Pipeline Tests', () {
    test('validateImage returns Right(true) for clear image', () async {
      final result = await repository.validateImage('/valid/card.jpg');
      expect(result.isRight(), isTrue);
    });

    test('validateImage returns Left(BlurredImageFailure) for blurry image', () async {
      final result = await repository.validateImage('/blurry/card.jpg');
      expect(result.isLeft(), isTrue);
    });

    test('recognizeText via GoogleMlKit Strategy returns recognized text', () async {
      final result = await repository.recognizeText(
        imagePath: '/valid/card.jpg',
        provider: OcrProviderType.googleMlKit,
      );
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (rawText) => expect(rawText.fullText, contains('Alex Morgan')),
      );
    });

    test('recognizeText via Tesseract Strategy returns recognized text', () async {
      final result = await repository.recognizeText(
        imagePath: '/valid/card.jpg',
        provider: OcrProviderType.tesseract,
      );
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (rawText) => expect(rawText.fullText, contains('Alex Morgan')),
      );
    });

    test('extractEntities maps raw text to ExtractedLeadEntity', () async {
      const rawText = RawOcrText(
        fullText: 'Alex Morgan\nNexus Tech Solutions Inc.',
        lines: ['Alex Morgan', 'Nexus Tech Solutions Inc.'],
        confidence: 0.95,
      );
      final result = await repository.extractEntities(rawText, '/valid/card.jpg');
      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should not fail'),
        (lead) {
          expect(lead.fullName.value, 'Alex Morgan');
          expect(lead.company.value, 'Nexus Tech Solutions Inc.');
          expect(lead.overallConfidence, 0.96);
        },
      );
    });
  });
}
