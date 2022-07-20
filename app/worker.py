import os
from time import sleep
from random import randint
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from celery import Celery


celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[
        CeleryIntegration()],
    send_default_pii=True,
    environment=os.environ.get("SENTRY_ENV"))


@celery_app.task(name="create_task")
def create_task(task_type):
    sleep(int(task_type) * 10)
    return True


@celery_app.task(name="plus")
def plus(x, y):
    sleep(randint(1, 30))
    return x + y


@celery_app.task(name="minus")
def minus(x, y):
    sleep(randint(1, 30))
    return x - y


@celery_app.task(name="divide")
def divide(x, y):
    sleep(randint(1, 30))
    return x / y


@celery_app.task(name="multiply")
def multiply(x, y):
    sleep(randint(1, 30))
    return x * y
