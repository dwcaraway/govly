# -*- coding: utf-8 -*-

__author__ = 'Dave Caraway'

from dougrain import Builder
from app.api.base import BaseView
from flask import url_for

class RootView(BaseView):
    """Index of all endpoints"""

    def index(self):
        """Starting endpoint for all available endpoints"""
        return Builder('/').add_curie('r', '/rels/{rel}') \
            .add_link('r:organizations', url_for('OrganizationsView:index'))\
            .set_property('welcome', 'Welcome to the Vitals API!')\
            .as_object()