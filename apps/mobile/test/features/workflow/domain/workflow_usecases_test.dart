import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/workflow/data/repositories/task_repository_impl.dart';
import 'package:leadscan_mobile/features/workflow/domain/usecases/get_calendar_agenda_usecase.dart';
import 'package:leadscan_mobile/features/workflow/domain/usecases/get_reminders_usecase.dart';
import 'package:leadscan_mobile/features/workflow/domain/usecases/get_task_details_usecase.dart';
import 'package:leadscan_mobile/features/workflow/domain/usecases/get_tasks_usecase.dart';

void main() {
  late TaskRepositoryImpl repository;
  late GetTasksUseCase getTasksUseCase;
  late GetTaskDetailsUseCase getTaskDetailsUseCase;
  late GetCalendarAgendaUseCase getCalendarAgendaUseCase;
  late GetRemindersUseCase getRemindersUseCase;

  setUp(() {
    repository = TaskRepositoryImpl();
    getTasksUseCase = GetTasksUseCase(repository);
    getTaskDetailsUseCase = GetTaskDetailsUseCase(repository);
    getCalendarAgendaUseCase = GetCalendarAgendaUseCase(repository);
    getRemindersUseCase = GetRemindersUseCase(repository);
  });

  group('Workflow UseCases Unit Tests', () {
    test('GetTasksUseCase returns tasks list', () async {
      final res = await getTasksUseCase();
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (tasks) => expect(tasks.isNotEmpty, isTrue),
      );
    });

    test('GetTaskDetailsUseCase returns task details for ID', () async {
      final res = await getTaskDetailsUseCase('task_201');
      expect(res.isRight(), isTrue);
      res.fold(
        (failure) => fail('Should not fail'),
        (task) => expect(task.title, isNotEmpty),
      );
    });

    test('GetCalendarAgendaUseCase returns agenda items', () async {
      final res = await getCalendarAgendaUseCase(DateTime.now());
      expect(res.isRight(), isTrue);
    });

    test('GetRemindersUseCase returns active reminders', () async {
      final res = await getRemindersUseCase();
      expect(res.isRight(), isTrue);
    });
  });
}
