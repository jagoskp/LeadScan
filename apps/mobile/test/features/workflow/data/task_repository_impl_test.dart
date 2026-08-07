import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/workflow/data/repositories/task_repository_impl.dart';

void main() {
  late TaskRepositoryImpl repository;

  setUp(() {
    repository = TaskRepositoryImpl();
  });

  group('TaskRepositoryImpl Unit Tests', () {
    test('getTasks returns list of tasks from remote data source', () async {
      final res = await repository.getTasks();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Failed to fetch tasks'),
        (tasks) => expect(tasks.length, greaterThanOrEqualTo(2)),
      );
    });

    test('updateTaskStatus updates status correctly', () async {
      final res = await repository.updateTaskStatus('task_201', 'Completed');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Update failed'),
        (task) => expect(task.status, equals('Completed')),
      );
    });
  });
}
