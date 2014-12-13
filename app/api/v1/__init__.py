# -*- coding: utf-8 -*-
"""
    vitals.api.v1
    ~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import importlib
import inspect
import pkgutil

def get_views():
    """
    Get all view classes within a given module
    params

    :returns an array of class
    """
    rv = []
    for _, m, _ in pkgutil.iter_modules(path=__path__):
        i = importlib.import_module(name="{0}.{1}".format(__name__, m))
        for name, obj in inspect.getmembers(i, predicate=inspect.isclass):
            if u'View' in name and obj.__module__ == i.__name__:
                rv.append(obj)

    return rv

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
    for v in get_views():
        v.register(bp)

    return bp
