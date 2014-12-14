# -*- coding: utf-8 -*-
"""
    vitals.frontend
    ~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import logging

from . import extensions
from . import views
from frontend import assets


_log = logging.getLogger(__name__)


def create_app(settings_override=None):
    """Returns a vitals frontend application instance"""

    from .. import framework

    app = framework.create_app(__name__, __path__, settings_override,
                               security_register_blueprint=True)
    # Init assets
    assets.init_app(app)

    # Flask-DebugToolbar
    extensions.debug_toolbar.init_app(app)

    # Initialize Views
    views.init_app(app)

    _log.info("Flask frontend app created")
    return app
