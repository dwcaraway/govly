# -*- coding: utf-8 -*-
"""
    tests.settings
    ~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from app.settings import Config

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'testing-secret-key'

    CLIENT_DOMAIN = 'http://localhost:9000'

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    BROKER_BACKEND='memory'
    CELERY_BROKER_URL = ""

    SQLALCHEMY_POOL_SIZE = None
    SQLALCHEMY_POOL_TIMEOUT = None
    SQLALCHEMY_POOL_RECYCLE = None
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    SECURITY_PASSWORD_HASH = 'plaintext'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'
