from typing import Any
from celery.schedules import crontab


def setup_scheduler(app: Any) -> None:
    """Register periodic cron and delayed cleanup jobs into Celery Beat config."""
    app.conf.beat_schedule = {
        "cleanup-notifications-daily": {
            "task": "services.worker.src.celery_app.execute_registered_task",
            "schedule": crontab(hour="2", minute="0"),  # Every day at 2:00 AM
            "args": ("maintenance.clean_old_notifications",),
            "options": {"queue": "maintenance"},
        },
        "purge-dlq-weekly": {
            "task": "services.worker.src.celery_app.execute_registered_task",
            "schedule": crontab(day_of_week="sunday", hour="3", minute="0"),
            "args": ("maintenance.purge_dlq_tasks",),
            "options": {"queue": "maintenance"},
        },
        "realign-quotas-daily": {
            "task": "services.worker.src.celery_app.execute_registered_task",
            "schedule": crontab(hour="1", minute="0"),  # Every day at 1:00 AM
            "args": ("maintenance.perform_storage_quota_realignments",),
            "options": {"queue": "maintenance"},
        },
    }
