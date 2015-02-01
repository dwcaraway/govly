# -*- coding: utf-8 -*-
"""
    vitals.frontend.security
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from flask import request, render_template, Flask
from flask.ext.classy import route
from flask.ext.jwt import generate_token, SignatureExpired, BadSignature
from flask.ext.restful.reqparse import RequestParser
from flask.ext.security import current_user
from flask_security.registerable import encrypt_password
from ..base import BaseView, secure_endpoint
from .rel import RELS
from app.models.users import User
from jsonschema import validate, ValidationError, FormatChecker
from urlparse import urljoin

from itsdangerous import URLSafeTimedSerializer, TimestampSigner
from flask import current_app, url_for
from app.framework.utils import send_message
from datetime import datetime

request_register_options = RequestParser()
request_register_options.add_argument('email', type=str, location='json', required=True)
request_register_options.add_argument('password', type=str, location='json', required=True)

request_confirm_options = RequestParser()
request_confirm_options.add_argument('token', type=str, location='args', required=True)

SECONDS_IN_A_DAY = 86400

class AuthView(BaseView):

    ts = None

    # @route('/jwt/token', methods=['POST'])
    # def jwt_token(self):
    #     """
    #     Given valid user credentials, return a JWT token
    #     """
    #     options = request_register_options.parse_args()
    #
    #     #TODO attempt user login
    #     if not current_user.is_authenticated():
    #         return {
    #             "status": 401,
    #             "message": "No user authenticated",
    #         }, 401, {"WWW-Authenticate": "None"}
    #
    #     return dict(token=generate_token(current_user))

    @route('/register', methods=['POST'])
    def register_user(self):

        schema = RELS['v1.AuthView:register'][request.method]
        data = request_register_options.parse_args()

        try:
            validate(data, schema, format_checker=FormatChecker())

            if User.query.filter_by(email=data['email']).first():
                return {'status': 409, 'message':'An account with that email already exists.'}, 409

            password = encrypt_password(data['password'])

            #TODO need to accept first and last name on register
            user = User.create(email=data['email'], password=password, first_name='samplefirstname', last_name="samplelastname")
            confirmation_link = self.generate_confirmation_link(user)

            send_message(
                subject='Please Confirm Your Fogmine Account',
                sender="do-not-reply@fogmine.com",
                recipients = [user.email],
                html_body=render_template('email/activate.html', user=user, confirmation_link=confirmation_link),
                text_body=render_template('email/activate.txt', user=user, confirmation_link=confirmation_link)
            )

            return {'status': 201, 'message':'A confirmation email has been sent.'}, 201
        except ValidationError as e:
            return {
                'status': 400,
                'message': e.message
            }, 400

    @route('/confirm', methods=['GET'])
    def confirm_email(self):
        if not self.ts:
            self.ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        args = request_confirm_options.parse_args()
        token = args.get('token')

        try:
            email_signed = self.ts.loads(token, salt="email-confirm-key", max_age=SECONDS_IN_A_DAY*3)

            groups = email_signed.split('.')
            email = '.'.join(groups[:-2])

            user = User.query.filter_by(email=email).first_or_404()

            if not user:
                raise BadSignature

            s = TimestampSigner(secret_key=user.secret)
            s.unsign(email_signed, max_age=SECONDS_IN_A_DAY*3)

            if user.confirmed_at:
                return {
                    'status': 409,
                    'message': 'Email already confirmed'
                }, 409

            user.confirmed_at = datetime.now()
            user.save()
        except BadSignature:
            return {
                'status': 409,
                'message': "Invalid confirmation token"
            }, 409
        except SignatureExpired:
            return {
                'status': 409,
                'message': "Confirmation token has expired."
            }, 409

        return {'status': 200, 'message': 'Account confirmed.', 'token': generate_token(user)}

    @route('/change', methods=['POST'])
    @secure_endpoint()
    def change_password(self):
        #TODO
        return {'TO': 'DO'}, 501

    @route('/reset', methods=['POST'])
    def reset_password(self):
        #TODO
        return {'TO': 'DO'}, 501

    @route('/logout', methods=['GET'])
    @secure_endpoint()
    def logout(self):
        #TODO see 85848860
        return {'TO': 'DO'}, 501

    def generate_confirmation_link(self, user):
        """Generates a random link for confirming emails with timestamp for expiry"""
        if not self.ts:
            self.ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        s = TimestampSigner(secret_key=user.secret)

        token = self.ts.dumps(s.sign(user.email), salt=current_app.config["EMAIL_CONFIRM_SALT"])
        return urljoin(current_app.config['CLIENT_DOMAIN'], '/#/confirm?token='+token)

