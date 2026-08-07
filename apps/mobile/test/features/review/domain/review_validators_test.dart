import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/ocr/domain/entities/ocr_result_entity.dart';
import 'package:leadscan_mobile/features/review/data/repositories/review_repository_impl.dart';
import 'package:leadscan_mobile/features/review/domain/entities/review_lead_entity.dart';

void main() {
  late ReviewRepositoryImpl repository;

  setUp(() {
    repository = ReviewRepositoryImpl();
  });

  ReviewLeadEntity createDummyLead({
    String fullName = 'Alex Morgan',
    String company = 'Nexus Tech',
    String email = 'alex@nexustech.io',
    String phone = '+15552345678',
    String website = 'www.nexustech.io',
    String pinCode = '94107',
  }) {
    return ReviewLeadEntity(
      id: '1',
      imagePath: '/path',
      fullName: fullName,
      company: company,
      designation: 'Architect',
      email: email,
      phone: phone,
      mobile: '',
      website: website,
      address: '100 Street',
      city: 'SF',
      state: 'CA',
      country: 'USA',
      pinCode: pinCode,
      notes: '',
      customFields: const {},
      unknownFields: const [],
      overallConfidence: 0.95,
      fieldConfidences: const {},
      rawOcr: const RawOcrText(fullText: '', lines: [], confidence: 0.95),
      createdAt: DateTime.now(),
    );
  }

  group('Review Validation Tests', () {
    test('validates valid lead successfully', () {
      final lead = createDummyLead();
      final results = repository.validateLead(lead);

      expect(results['fullName']?.isValid, isTrue);
      expect(results['company']?.isValid, isTrue);
      expect(results['email']?.isValid, isTrue);
      expect(results['phone']?.isValid, isTrue);
      expect(results['website']?.isValid, isTrue);
      expect(results['pinCode']?.isValid, isTrue);
    });

    test('fails validation when fullName is empty', () {
      final lead = createDummyLead(fullName: '');
      final results = repository.validateLead(lead);

      expect(results['fullName']?.isValid, isFalse);
      expect(results['fullName']?.errorMessage, 'Full Name is required');
    });

    test('fails validation when email format is invalid', () {
      final lead = createDummyLead(email: 'invalid-email');
      final results = repository.validateLead(lead);

      expect(results['email']?.isValid, isFalse);
      expect(results['email']?.errorMessage, 'Invalid email address format');
    });

    test('generates AI warnings when contact fields are missing', () {
      final lead = createDummyLead(email: '', phone: '');
      final warnings = repository.generateAiWarnings(lead);

      expect(warnings.any((w) => w.fieldName == 'Email'), isTrue);
      expect(warnings.any((w) => w.fieldName == 'Phone'), isTrue);
    });
  });
}
