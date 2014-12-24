# -*- coding: utf-8 -*-
"""
    vitals.framework.factory
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import logging
import os

from flask import Flask
from flask.ext.security import SQLAlchemyUserDatastore
from raven.contrib.flask import Sentry

from .extensions import *
from .middleware import HTTPMethodOverrideMiddleware
from .security import authenticate, load_user, make_payload
from ..models.users import User, Role

_log = logging.getLogger(__name__)

__all__ = ('create_app',)

def create_app(package_name, package_path, settings_override=None,
               security_register_blueprint=False):
    """
    Returns a :class:`Flask` application instance configured with common
    functionality for the webapp.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param security_register_blueprint: register views for flask-security
    """
    # Instance Path
    instance_path = os.environ.get("VITALS_INSTANCE_PATH", None)

    app = Flask(package_name, instance_relative_config=True,
                instance_path=instance_path)

    # Initialize settings
    app.config.from_object(settings_override)

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Flask-Mail
    mail.init_app(app)

    # Flask-Security
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=security_register_blueprint)

    # Flask-JWT
    jwt.init_app(app)
    jwt.authentication_handler(authenticate)
    jwt.payload_handler(make_payload)
    jwt.user_handler(load_user)

    # Flask-CORS
    cors.init_app(app, supports_credentials=True)

    # Flask-SSLify to force SSL - only for production
    if not app.debug and not app.testing:
        from flask_sslify import SSLify
        SSLify(app, permanent=True)

    # Sentry - only for production
    if not app.debug and not app.testing and 'SENTRY_DSN' in app.config:
        sentry = Sentry(app)

    # Middleware
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    _log.info("Flask framework app created.")
    return app
