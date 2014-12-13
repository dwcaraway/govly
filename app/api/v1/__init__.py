# -*- coding: utf-8 -*-
"""
    vitals.api.v1
    ~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from app.api.v1.todos import TodosView
from app.api.v1.organizations import OrganizationsView
from app.api.v1.root import RootView
from app.api.v1.rel import LinkRelationsView

def create_blueprint(name=None, url_prefix=None, subdomain=None):
    """Register API endpoints on a Flask :class:`Blueprint`."""

    from flask import Blueprint

    # Determine blueprint name
    name = name or __name__.split('.')[-1]
    if subdomain:
        name = "{0}_{1}".format(subdomain, name)

    # Create blueprint
    bp = Blueprint(name, __name__, url_prefix=url_prefix, subdomain=subdomain)

    # Register API endpoints
    TodosView.register(bp)
    OrganizationsView.register(bp)
    LinkRelationsView.register(bp)
    RootView.register(bp)

    return bp
