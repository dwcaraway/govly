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
from flask.ext.jwt import SignatureExpired, BadSignature, current_user
from flask.ext.restful.reqparse import RequestParser
from flask_security.registerable import encrypt_password, register_user
import werkzeug
from werkzeug.exceptions import Conflict

from flask_security.changeable import change_user_password
from flask_security.recoverable import update_password, reset_password_token_status, generate_reset_password_token, send_password_reset_notice
from flask_security.confirmable import generate_confirmation_token, confirm_email_token_status, confirm_user
from flask_security.utils import verify_password, logout_user, get_token_status
from ..base import BaseView, secure_endpoint
from .rel import RELS
from app.models.users import User, Role, Invite
from jsonschema import validate, ValidationError, FormatChecker
from sqlalchemy.exc import IntegrityError
from urlparse import urljoin

from itsdangerous import URLSafeTimedSerializer, TimestampSigner
from flask import current_app, url_for
from app.framework.utils import send_message
from app.framework.security import generate_response_dict
from datetime import datetime

request_register_options = RequestParser()
request_register_options.add_argument('email', type=str, location='json', required=True)
request_register_options.add_argument('password', type=str, location='json', required=True)
request_register_options.add_argument('firstName', type=str, location='json', required=True)
request_register_options.add_argument('lastName', type=str, location='json', required=True)
request_register_options.add_argument('token', type=str, location='json', required=True)

request_confirm_options = RequestParser()
request_confirm_options.add_argument('token', type=str, location='json', required=True)

#Change password
change_password_options = RequestParser()
change_password_options.add_argument('old', type=str, location='json', required=True)
change_password_options.add_argument('new', type=str, location='json', required=True)

#Request the password reset
request_reset_password_options = RequestParser()
request_reset_password_options.add_argument('email', type=str, location='json', required=True)

#Do the password reset
reset_password_options = RequestParser()
reset_password_options.add_argument('password', type=str, location='json', required=True)
reset_password_options.add_argument('token', type=str, location='json', required=True)

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

        try:
            data = request_register_options.parse_args()
            validate(data, schema, format_checker=FormatChecker())

            invite_token = data['token']

            expired, invalid, invitor = get_token_status(invite_token, 'invite', 'USE_INVITE')

            if invalid or not invitor:
                return dict(status=409, message="Invite is invalid"), 409

            if expired:
                return dict(status=409, message="Invite has expired"), 409

            inviteTokenObj = Invite.find(token=invite_token).first()

            if not inviteTokenObj:
                return dict(status=409, message="Invite not found"), 409

            if inviteTokenObj.invitee_id:
                return dict(status=409, message="Invite already used"), 409

            password = encrypt_password(data['password'])
            user = register_user(email=data['email'], password=password, first_name=data['firstName'],
                   last_name=data['lastName'], roles=[Role.first(name='user')])

            inviteTokenObj.invitee_id = user.id
            inviteTokenObj.save()

            token = generate_confirmation_token(user)
            confirmation_link = urljoin(current_app.config['CLIENT_DOMAIN'], '/#/confirm?token='+token)

            #TODO this mail send should be performed asynchronously using celery, see issue #88850472
            send_message(
                subject='Please Confirm Your FogMine Account',
                sender="do-not-reply@fogmine.com",
                recipients = [user.email],
                html_body=render_template('email/activate.html', user=user, confirmation_link=confirmation_link),
                text_body=render_template('email/activate.txt', user=user, confirmation_link=confirmation_link)
            )

            user_data = generate_response_dict(user=user)

            return dict(status=201, message='A confirmation email has been sent to '+user.email, user=user_data), 201

        except ValidationError as e:
            return dict(status=400, message=e.message), 400
        except IntegrityError:
            return {'status': 409, 'message': 'An account with that email already exists.'}, 409
        except werkzeug.exceptions.ClientDisconnected:
            return dict(status=400, message='one or more required arguments missing from this request'), 400

    @route('/confirm', methods=['POST'])
    def confirm_email(self):

        schema = RELS['v1.AuthView:confirm'][request.method]
        args = request_confirm_options.parse_args()

        try:
            validate(args, schema, format_checker=FormatChecker())
            token = args.get('token')
            expired, invalid, user = confirm_email_token_status(token)

            if invalid or not user:
                return dict(status=409, message="Invalid confirmation token"), 409

            if expired:
                return dict(status=409, message="Confirmation token has expired"), 409

            confirmed = confirm_user(user)
            user.save()

            if not confirmed:
                return dict(status=409, message='Email already confirmed'), 409

        except ValidationError as e:
            return dict(status=400, message=e.message), 400

        return {'status': 200, 'message': 'Account confirmed.', 'user': generate_response_dict(user=user)}

    @route('/change', methods=['POST'])
    @secure_endpoint()
    def change_password(self):
        schema = RELS['v1.AuthView:change'][request.method]
        args = change_password_options.parse_args()

        try:
            validate(args, schema, format_checker=FormatChecker())
        except ValidationError as e:
            return dict(status=400, message=e.message), 400

        if not verify_password(args.get('old'), current_user.password):
            return dict(status=409, message='Invalid credentials'), 409

        change_user_password(current_user, password=args.get('new'))
        return {'status': 200, 'message': 'Password updated', 'user': generate_response_dict(user=current_user)}

    @route('/update', methods=['POST'])
    def update_password(self):
        """Used in conjunction with reset password to set password to a known value"""
        schema = RELS['v1.AuthView:update'][request.method]
        args = reset_password_options.parse_args()

        try:
            validate(args, schema, format_checker=FormatChecker())
        except ValidationError as e:
            return dict(status=400, message=e.message), 400

        token = args.get('token')
        expired, invalid, user = reset_password_token_status(token)

        if invalid or not user:
            return dict(status=409, message="Invalid reset token"), 409

        if expired:
            return dict(status=409, message="Reset token has expired"), 409

        update_password(user, args.get('password'))
        user.reset_secret()
        send_password_reset_notice(user)

        return {'status': 200, 'message': 'Password updated', 'user': generate_response_dict(user=user)}

    @route('/reset', methods=['POST'])
    def reset_request(self):
        """Sends a reset password email"""

        schema = RELS['v1.AuthView:reset'][request.method]
        args = request_reset_password_options.parse_args()
        email = args.get('email')

        user = User.find(email=email).first()

        if not user:
            return dict(status=409, message="Invalid email address"), 409

        token = generate_reset_password_token(user)

        reset_link = urljoin(current_app.config['CLIENT_DOMAIN'], '/#/reset/'+token)

        #TODO this mail send should be performed asynchronously using celery, see issue #88850472
        send_message(
            subject='FogMine Reset Request',
            sender="do-not-reply@fogmine.com",
            recipients = [user.email],
            html_body=render_template('email/reset.html', user=user, reset_link=reset_link),
            text_body=render_template('email/reset.txt', user=user, reset_link=reset_link)
        )

        return dict(status=200, message="Reset instructions sent")

    @route('/logout', methods=['GET'])
    @secure_endpoint()
    def logout(self):
        current_user.reset_secret()
        logout_user()

        return dict(status=200, message='You have been logged out')
