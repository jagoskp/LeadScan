import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/leads/data/repositories/lead_repository_impl.dart';
import 'package:leadscan_mobile/features/leads/domain/usecases/bulk_operate_leads_usecase.dart';
import 'package:leadscan_mobile/features/leads/domain/usecases/get_lead_details_usecase.dart';
import 'package:leadscan_mobile/features/leads/domain/usecases/get_lead_timeline_usecase.dart';
import 'package:leadscan_mobile/features/leads/domain/usecases/get_leads_usecase.dart';

void main() {
  late LeadRepositoryImpl repository;
  late GetLeadsUseCase getLeadsUseCase;
  late GetLeadDetailsUseCase getLeadDetailsUseCase;
  late BulkOperateLeadsUseCase bulkOperateUseCase;
  late GetLeadTimelineUseCase getTimelineUseCase;

  setUp(() {
    repository = LeadRepositoryImpl();
    getLeadsUseCase = GetLeadsUseCase(repository);
    getLeadDetailsUseCase = GetLeadDetailsUseCase(repository);
    bulkOperateUseCase = BulkOperateLeadsUseCase(repository);
    getTimelineUseCase = GetLeadTimelineUseCase(repository);
  });

  group('Lead Repository UseCases Unit Tests', () {
    test('GetLeadsUseCase returns list of leads', () async {
      final res = await getLeadsUseCase();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (leads) => expect(leads.isNotEmpty, isTrue),
      );
    });

    test('GetLeadDetailsUseCase returns lead details for ID', () async {
      final res = await getLeadDetailsUseCase('lead_101');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (lead) => expect(lead.fullName, isNotEmpty),
      );
    });

    test('BulkOperateLeadsUseCase executes action on lead IDs', () async {
      final res = await bulkOperateUseCase(leadIds: ['lead_101', 'lead_102'], action: 'favorite');
      expect(res.isRight(), isTrue);
    });

    test('GetLeadTimelineUseCase returns timeline items', () async {
      final res = await getTimelineUseCase('lead_101');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (timeline) => expect(timeline.isNotEmpty, isTrue),
      );
    });
  });
}
