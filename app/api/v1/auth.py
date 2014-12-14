# -*- coding: utf-8 -*-
"""
    vitals.frontend.security
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from flask import jsonify
from flask.ext.classy import route
from flask.ext.jwt import generate_token
from flask.ext.restful.reqparse import RequestParser
from flask.ext.security import current_user
from ..base import BaseView

request_options = RequestParser()
request_options.add_argument('Content-Type', type=str, location='headers')

class AuthView(BaseView):

    @route('/jwt/token', methods=['POST'])
    def jwt_token(self):
        """
        Returns a JWT token if the user is logged in and the post has
        content type application/json.  All errors are returned as json.
        """
        if not current_user.is_authenticated():
            return {
                "status": 401,
                "message": "No user authenticated",
            }, 401, {"WWW-Authenticate": "None"}
        options = request_options.parse_args()
        content_json = options.get('Content-Type') == 'application/json'
        if not content_json:
            return {
                "status": 415,
                "message": "Unsupported media type",
            }, 415
        return dict(token=generate_token(current_user))
