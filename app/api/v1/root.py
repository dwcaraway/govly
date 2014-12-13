# -*- coding: utf-8 -*-

__author__ = 'Dave Caraway'

from dougrain import Builder
from app.api.base import BaseView
from flask import url_for
from flask.ext.classy import route

class RootView(BaseView):
    """Index of all endpoints"""

    route_base='/'

    @route('/')
    def index(self):
        """Starting endpoint for all available endpoints"""
        return Builder(url_for('v1.RootView:index')).add_curie('r', '/rels/{rel}') \
            .add_link('r:organizations', url_for('v1.OrganizationsView:index'))\
            .set_property('welcome', 'Welcome to the FogMine API!')\
            .as_object()