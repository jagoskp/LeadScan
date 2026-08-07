import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/leads/data/repositories/lead_repository_impl.dart';
import 'package:leadscan_mobile/features/leads/domain/entities/lead_filter_options_entity.dart';

void main() {
  late LeadRepositoryImpl repository;

  setUp(() {
    repository = LeadRepositoryImpl();
  });

  group('LeadRepositoryImpl Unit Tests', () {
    test('getLeads returns all leads when filter is empty', () async {
      final res = await repository.getLeads();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Failed to load leads'),
        (leads) => expect(leads.length, greaterThanOrEqualTo(3)),
      );
    });

    test('getLeads filters by searchQuery correctly', () async {
      final res = await repository.getLeads(
        filterOptions: const LeadFilterOptionsEntity(searchQuery: 'Alex'),
      );
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Search failed'),
        (leads) {
          expect(leads.isNotEmpty, isTrue);
          expect(leads.first.fullName, contains('Alex'));
        },
      );
    });

    test('toggleFavorite updates favorite status', () async {
      final res = await repository.toggleFavorite('lead_102');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Toggle favorite failed'),
        (lead) => expect(lead.isFavorite, isTrue),
      );
    });
  });
}
