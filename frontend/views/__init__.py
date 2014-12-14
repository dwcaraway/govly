# -*- coding: utf-8 -*-                                                                                       
"""
    frontend.views
    ~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from .frontend.views.auth import AuthView
from .frontend.views.legal import LegalView
from .frontend.views.todos import TodosView

def init_app(app):
    AuthView.register(app)
    LegalView.register(app)
    TodosView.register(app)
