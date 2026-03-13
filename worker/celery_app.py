import os
from celery import Celery

app = Celery("jobradar")

app.conf.update(
    broker_url="redis://redis:6379/1",       # откуда брать задачи
    result_backend="redis://redis:6379/2",   # куда складывать результаты
    task_serializer="json",
    timezone="UTC",
)