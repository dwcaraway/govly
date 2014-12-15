# -*- coding: utf-8 -*-
"""
    tests.settings
    ~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
class TestingConfig:
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'testing-secret-key'

    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
    BROKER_BACKEND='memory'

    SQLALCHEMY_POOL_SIZE = None
    SQLALCHEMY_POOL_TIMEOUT = None
    SQLALCHEMY_POOL_RECYCLE = None
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    SECURITY_PASSWORD_HASH = 'plaintext'
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = False
    SECURITY_CHANGEABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_FLASH_MESSAGES = True
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

    JWT_AUTH_HEADER_PREFIX = 'Bearer'
