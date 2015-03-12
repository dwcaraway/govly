# -*- coding: utf-8 -*-
"""
    vitals.framework.security
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import logging

from flask import current_app,jsonify, _request_ctx_stack
from flask.ext.jwt import JWTError, current_user, generate_token
from flask.ext.security.utils import verify_and_update_password
from werkzeug.local import LocalProxy

_log = logging.getLogger(__name__)
_security = LocalProxy(lambda: current_app.extensions['security'])
_datastore = LocalProxy(lambda: _security.datastore)

def authenticate(username, password):
    user = _datastore.get_user(username)

    if user and verify_and_update_password(password, user) and user.roles:
        _log.info("%s authenticated successfully", username)
        _request_ctx_stack.top.current_user = user
        return user

    if not user:
        _log.warn("Authentication failed; unknown username %s", username)
    else:
        _log.warn("Authentication failed; invalid password for %s", username)
        if not user.roles:
            _log.warn("Authentication failed; No user roles found.")

def load_user(payload):
    user = _datastore.get_user(payload['user_id'])
    if user and user.secret == payload['secret']:
        return user
    if user:
        raise JWTError('Invalid JWT', 'Invalid secret')


def make_payload(user):
    """Returns a dictionary to be encoded based on the user."""
    return {
        "user_id": user.id,
        "secret": user.secret
    }

def make_response(payload):
    """Returns a flask response with the JSON web token and other fields"""

    resp = generate_response_dict(user=current_user, payload=payload)
    return jsonify(resp)


def generate_response_dict(user, payload=None):
    _payload = payload
    if not _payload:
        _payload = generate_token(user)

    masked_roles = [dict(bitMask=role.bitmask, title=role.name) for role in user.roles]

    return dict(token=_payload, roles=masked_roles, name=user.first_name)
