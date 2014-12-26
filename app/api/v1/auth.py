# -*- coding: utf-8 -*-
"""
    vitals.frontend.security
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from flask import request
from flask.ext.classy import route
from flask.ext.jwt import generate_token
from flask.ext.restful.reqparse import RequestParser
from flask.ext.security import current_user
from flask_security.registerable import register_user
from ..base import BaseView, secure_endpoint
from .rel import RELS
from jsonschema import validate, ValidationError, FormatChecker

request_jwt_token_options = RequestParser()
request_jwt_token_options.add_argument('Content-Type', type=str, location='headers')

request_register_options = RequestParser()
request_register_options.add_argument('email', type=str, location='json', required=True)
request_register_options.add_argument('password', type=str, location='json', required=True)

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
        options = request_jwt_token_options.parse_args()
        content_json = '/json' in options.get('Content-Type')
        if not content_json:
            return {
                "status": 415,
                "message": "Unsupported media type",
            }, 415
        return dict(token=generate_token(current_user))

    @route('/register', methods=['POST'])
    def register_user(self):
        data = request_register_options.parse_args()
        schema = RELS['v1.AuthView:register'][request.method]

        try:
            validate(data, schema, format_checker=FormatChecker())
            register_user(email=data['email'], password=data['password'])
            return {'status': 201, 'message':'A confirmation email has been sent.'}, 201
        except ValidationError as e:
            return {
                'status': 400,
                'message': e.message
            }, 400

    @route('/confirm', methods=['POST'])
    def confirm_user(self):
        #TODO
        return {'TO':'DO'}, 501

    @route('/change', methods=['POST'])
    @secure_endpoint()
    def change_password(self):
        #TODO
        return {'TO':'DO'}, 501

    @route('/reset', methods=['POST'])
    def reset_password(self):
        #TODO
        return {'TO':'DO'}, 501

