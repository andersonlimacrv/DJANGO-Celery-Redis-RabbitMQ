""" projeto/
├── queues_mqtt/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── mqtt/
│   ├── __init__.py
│   ├── tasks.py
│   └── ...
├── celery.py
├── manage.py
└── ... """

from celery import shared_task

@shared_task
def add (x, y):
    return x + y