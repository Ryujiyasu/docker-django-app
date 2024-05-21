from celery import shared_task  # type: ignore
import time

@shared_task
def hello_world():
    print("start hello_world")
    print("hello")
    print("-----" * 200)
    print("end hello_world")
    return "hello world"


@shared_task
def calc(a: int, b: int) -> int:
    result: int = a + b
    return result

@shared_task
def example_task():
    return "Hello, Celery!"

@shared_task
def time_sleep_func(project_id: str) -> str:
    print(f"project_id - {project_id}")

    time.sleep(10)
    message: str = f"Hello - {project_id}"
    print(f"message - {message}")

    return message