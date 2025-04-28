from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_dramatiq.tasks import delete_old_tasks
from sentry_sdk import capture_exception

from typing import Any


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age: int = 604_800) -> None:
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param existing_job_ids: The IDs of the currently scheduled jobs.
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """

    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def sentry_listener(event: Any) -> None:
    # EVENT_JOB_ERROR as a filter should cover this but provides no guarantee
    if event.exception:
        capture_exception(event.exception)


def schedule_delete_old_tasks() -> None:
    """
    Delete old tasks from the database once a day (this is the default if we don't pass any arguments)
    """

    delete_old_tasks.send()


class Command(BaseCommand):
    help = "Runs APScheduler."

    # if you add a new task you HAVE to restart the scheduler container
    def handle(self, *args: Any, **options: Any) -> None:
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        django_job_store = DjangoJobStore()
        scheduler.add_jobstore(django_job_store, "default")

        scheduler.add_listener(sentry_listener, mask=EVENT_JOB_ERROR)

        # Clear out old scheduled jobs that may have been removed
        django_job_store.remove_all_jobs()

        scheduler.add_job(
            schedule_delete_old_tasks,
            trigger=CronTrigger(hour=0, minute=0),
            id="delete_old_jobs",
            max_instances=1,
            replace_existing=True,
        )
        print("Added daily job: 'delete_old_jobs'.")

        try:
            print("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            print("Stopping scheduler...")
            scheduler.shutdown()
            print("Scheduler shut down successfully!")
