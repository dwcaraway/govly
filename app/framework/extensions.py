# -*- coding: utf-8 -*-
"""
    vitals.framework.extensions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.jwt import JWT
jwt = JWT()

from flask.ext.mail import Mail
mail = Mail()

from flask.ext.security import Security
security = Security()

from flask.ext.celery import Celery
celery = Celery()

from flask.ext.cors import CORS
cors = CORS()

__all__ = ("db", "migrate", "jwt", "mail", "security", "celery", 'cors')
