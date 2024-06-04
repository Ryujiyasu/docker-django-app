from celery import shared_task  # type: ignore

@shared_task
def appium() -> None:
    print("start appium")
    print("appium test")
    print("-----" * 200)
    print("end appium")