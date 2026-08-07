import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/image_processor.dart';
import 'package:leadscan_mobile/features/ocr/data/datasources/ocr_datasource.dart';
import 'package:leadscan_mobile/features/ocr/data/repositories/ocr_repository_impl.dart';
import 'package:leadscan_mobile/features/ocr/domain/usecases/process_image_ocr_usecase.dart';
import 'package:leadscan_mobile/features/ocr/presentation/controllers/ocr_processing_controller.dart';
import 'package:leadscan_mobile/features/ocr/presentation/pages/ocr_processing_page.dart';
import 'package:leadscan_mobile/features/ocr/presentation/providers/ocr_providers.dart';

void main() {
  Widget buildTestableWidget({required String imagePath}) {
    final repo = OcrRepositoryImpl(
      imageProcessor: ImageProcessor(),
      ocrDataSource: OcrDataSourceImpl(),
    );

    return ProviderScope(
      overrides: [
        ocrProcessingControllerProvider.overrideWith(
          (ref) => OcrProcessingController(
            processImageOcrUseCase: ProcessImageOcrUseCase(repo),
          ),
        ),
      ],
      child: MaterialApp(
        theme: AppTheme.lightTheme,
        home: OcrProcessingPage(imagePath: imagePath),
      ),
    );
  }

  group('OcrProcessingPage Widget Tests', () {
    testWidgets('renders processing screen with provider chips and stepper', (tester) async {
      await tester.pumpWidget(buildTestableWidget(imagePath: '/valid/card.jpg'));
      await tester.pump();

      expect(find.text('OCR & AI Extraction Pipeline'), findsOneWidget);
      expect(find.text('ML Kit'), findsOneWidget);
      expect(find.text('Tesseract'), findsOneWidget);
      expect(find.text('Cloud OCR'), findsOneWidget);

      await tester.pump(const Duration(seconds: 2));

      expect(find.text('Card Parsed Successfully!'), findsOneWidget);
      expect(find.text('Alex Morgan'), findsOneWidget);
      expect(find.text('Nexus Tech Solutions Inc.'), findsOneWidget);
    });
  });
}
