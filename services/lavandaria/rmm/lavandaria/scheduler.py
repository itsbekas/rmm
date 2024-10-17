from os import getenv

from celery.app import Celery

from rmm.lavandaria.service import fetch_device_status

REDIS_URL = getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

if REDIS_URL is None:
    print("REDIS_URL is not set")
    exit(1)

app = Celery("rmm.lavandaria.scheduler", broker=REDIS_URL, backend=REDIS_URL)
app.conf.timezone = "Europe/Lisbon"


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(120.0, get_devices.s(), expires=60.0)


@app.task
def get_devices():
    return fetch_device_status()
