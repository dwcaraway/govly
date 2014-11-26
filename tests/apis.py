# -*- coding: utf-8 -*-
"""
    test.apis
    ~~~~~~~~~

    :author: Dave Caraway
    :copyright: (c) 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from app import api


class SecureView(api.BaseView):

    @api.secure_endpoint()
    def index(self):
        return {
            "secret": "shhhhhh, keep this quiet",
        }

class SecureResource(api.BaseResource):

    @api.secure_endpoint()
    def get(self):
        return {
            "secret": "shhhhhh, keep this quiet",
        }


def classy_api(app):
    """Create an Flask-Classy-based API on app"""
    bp = api.v1.create_blueprint('test', url_prefix='/api/tests')
    SecureView.register(bp)
    api.register_blueprint(app, bp)
