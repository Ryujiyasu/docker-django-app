import time
from django.core.management.base import BaseCommand
from django_celery_results.models import TaskResult
from django.db.models import QuerySet

from celery.result import AsyncResult

from polls.tasks import appium


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('device', type=str, help='Device name for Appium test')

    def handle(self, *args, **options):  # type: ignore
        device = options['device']
        task: AsyncResult = appium.delay(device)  # type: ignore
        print("task.status", task.status)  # type: ignore

        task_id: str = task.id  # type: ignore
        print("task", task.id)  # type: ignore

        time.sleep(5)

        task_models: QuerySet[TaskResult] = TaskResult.objects.filter(task_id=task_id)
        for task_model in task_models:
            print("task_model.result", task_model.result)
            print("task_model.date_created", task_model.date_created)
            print("task_model.date_done", task_model.date_done)

        time.sleep(10)

        print("----" * 20)

        task_models = TaskResult.objects.filter(task_id=task_id)
        for task_model in task_models:
            print("task_model.result", task_model.result)
            print("task_model.date_created", task_model.date_created)
            print("task_model.date_done", task_model.date_done)