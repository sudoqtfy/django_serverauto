#!/usr/bin/env 

from sshauth import add_keys
import time 
from celery import Celery
import os
#celery -A tasks worker  --loglevel=info

broker = 'redis://127.0.0.1/0'
backend = 'redis://127.0.0.1/0'

app = Celery('tasks', backend=backend, broker=broker)

app.conf.update(
            CELERY_TASK_SERIALIZER='json',
            CELERY_ACCEPT_CONTENT=['json'],
            CELERY_RESULT_SERIALIZER='json',
        )

@app.task
def add_keys_task(host, user, password, key_files, port=22):
    return add_keys(host, user, password, key_files, port=22)
