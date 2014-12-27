# -*- coding: utf-8 -*-
"""
    tasks
    ~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.
"""
from .email import send_message
from .workq import create_celery_app
