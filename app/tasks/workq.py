# -*- coding: utf-8 -*-
"""
    tasks.workq
    ~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.
"""
from celery import Celery
import os
from app import create_app

def create_celery_app(app=None):
    app = app or create_app('vitals',
                            os.path.dirname(__file__))
    # Celery must be configured with the proper broker when it is initialized;
    # otherwise, bad things happen
    broker = app.config.get('CELERY_BROKER_URL', None)
    celery = Celery(__name__, broker=broker)
    celery.config_from_object(app.config, force=True)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = create_celery_app()
task = celery.task