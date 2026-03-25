from celery import Celery

app = Celery(
    "workers",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

app.autodiscover_tasks(["workers"])

app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)