# -*- coding: utf-8 -*-

__author__ = 'Dave Caraway'

from app.api.v1 import get_views
from app.api import BaseView
from flask import \
    (
    url_for,
     request
)
from flask.ext.classy import route
from dougrain import Builder

class RootView(BaseView):
    """Index of all endpoints"""

    route_base='/'

    @route('/')
    def index(self):
        """Starting endpoint for all available endpoints"""
        b = Builder(url_for('v1.RootView:index')).add_curie('r', url_for('v1.LinkRelationsView:get', id='foo')\
                                    .replace('foo', '{rel}')).set_property('welcome', 'Welcome to the FogMine API!')

        for cls in get_views():
            if cls.__name__ in ['RootView', 'AuthView']:
                continue

            prefix = cls.__name__[:-len('View')].lower()
            rel = 'r:{0}'.format(prefix)
            href = url_for('v1.{0}:index'.format(cls.__name__))
            b.add_link(rel, href)

        return b.as_object()
