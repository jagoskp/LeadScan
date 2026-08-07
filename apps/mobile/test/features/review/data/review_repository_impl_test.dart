import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/ocr/domain/entities/ocr_result_entity.dart';
import 'package:leadscan_mobile/features/review/data/datasources/temp_review_datasource.dart';
import 'package:leadscan_mobile/features/review/data/repositories/review_repository_impl.dart';
import 'package:leadscan_mobile/features/review/domain/entities/review_lead_entity.dart';

void main() {
  late ReviewRepositoryImpl repository;
  late TempReviewDataSource dataSource;

  setUp(() {
    dataSource = TempReviewDataSource();
    repository = ReviewRepositoryImpl(tempDataSource: dataSource);
  });

  ReviewLeadEntity createLead() {
    return ReviewLeadEntity(
      id: 'lead_1',
      imagePath: '/path/card.jpg',
      fullName: 'Alex Morgan',
      company: 'Nexus Tech',
      designation: 'Architect',
      email: 'alex@nexustech.io',
      phone: '+15552345678',
      mobile: '+15559876543',
      website: 'www.nexustech.io',
      address: '100 Plaza',
      city: 'San Francisco',
      state: 'CA',
      country: 'USA',
      pinCode: '94107',
      notes: 'Met at event',
      customFields: const {'Source': 'Scanner'},
      unknownFields: const [],
      overallConfidence: 0.95,
      fieldConfidences: const {'fullName': 0.98},
      rawOcr: const RawOcrText(fullText: '', lines: [], confidence: 0.95),
      createdAt: DateTime.now(),
    );
  }

  group('ReviewRepositoryImpl Unit Tests', () {
    test('approveLead returns ApprovedLeadEntity on valid lead', () {
      final lead = createLead();
      final result = repository.approveLead(lead);

      expect(result.isRight(), isTrue);
      result.fold(
        (failure) => fail('Should not fail'),
        (approvedLead) {
          expect(approvedLead.fullName, 'Alex Morgan');
          expect(approvedLead.readyForGoogleSync, isTrue);
          expect(dataSource.getLastApprovedLead(), isNotNull);
        },
      );
    });

    test('approveLead fails when required company field is empty', () {
      final lead = createLead().copyWith(company: '');
      final result = repository.approveLead(lead);

      expect(result.isLeft(), isTrue);
    });
  });
}
