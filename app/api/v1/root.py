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
        return Builder('/').add_curie('r', '/rels/{rel}') \
            .add_link('r:organizations', url_for('v1.OrganizationsView:index'))\
            .set_property('welcome', 'Welcome to the Vitals API!')\
            .as_object()