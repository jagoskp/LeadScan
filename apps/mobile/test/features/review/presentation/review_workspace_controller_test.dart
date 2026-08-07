import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/ocr/domain/entities/ocr_result_entity.dart';
import 'package:leadscan_mobile/features/review/data/repositories/review_repository_impl.dart';
import 'package:leadscan_mobile/features/review/domain/entities/review_lead_entity.dart';
import 'package:leadscan_mobile/features/review/domain/usecases/approve_lead_usecase.dart';
import 'package:leadscan_mobile/features/review/domain/usecases/validate_review_lead_usecase.dart';
import 'package:leadscan_mobile/features/review/presentation/controllers/review_workspace_controller.dart';
import 'package:leadscan_mobile/features/review/presentation/controllers/review_workspace_state.dart';

void main() {
  late ReviewWorkspaceController controller;

  setUp(() {
    final repo = ReviewRepositoryImpl();
    controller = ReviewWorkspaceController(
      repository: repo,
      validateUseCase: ValidateReviewLeadUseCase(repo),
      approveUseCase: ApproveLeadUseCase(repo),
    );
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
      customFields: const {},
      unknownFields: const ['Extra Block'],
      overallConfidence: 0.95,
      fieldConfidences: const {'fullName': 0.98},
      rawOcr: const RawOcrText(fullText: '', lines: [], confidence: 0.95),
      createdAt: DateTime.now(),
    );
  }

  group('ReviewWorkspaceController StateNotifier Tests', () {
    test('initializeWithLead sets lead in state and calculates validation', () {
      final lead = createLead();
      controller.initializeWithLead(lead);

      expect(controller.state.lead, lead);
      expect(controller.state.isValid, isTrue);
    });

    test('updateField modifies field and recalculates validation', () {
      controller.initializeWithLead(createLead());
      controller.updateField('fullName', 'John Doe');

      expect(controller.state.lead?.fullName, 'John Doe');
    });

    test('addCustomField adds key-value pair to customFields', () {
      controller.initializeWithLead(createLead());
      controller.addCustomField('Industry', 'FinTech');

      expect(controller.state.lead?.customFields['Industry'], 'FinTech');
    });

    test('assignUnknownFieldToTarget reassigns unknown text to field', () {
      controller.initializeWithLead(createLead());
      controller.assignUnknownFieldToTarget('Extra Block', 'notes');

      expect(controller.state.lead?.notes, 'Extra Block');
      expect(controller.state.lead?.unknownFields, isEmpty);
    });

    test('setActiveTab updates tab view', () {
      controller.setActiveTab(ReviewTab.compareOcr);
      expect(controller.state.activeTab, ReviewTab.compareOcr);
    });

    test('approveLead approves lead and sets isApproved true', () async {
      controller.initializeWithLead(createLead());
      final success = await controller.approveLead();

      expect(success, isTrue);
      expect(controller.state.isApproved, isTrue);
      expect(controller.state.approvedLead, isNotNull);
    });
  });
}
