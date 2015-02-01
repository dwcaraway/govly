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
from flask.ext.jwt import JWTError, current_user
from flask.ext.security.utils import verify_and_update_password
from werkzeug.local import LocalProxy

_log = logging.getLogger(__name__)
_security = LocalProxy(lambda: current_app.extensions['security'])
_datastore = LocalProxy(lambda: _security.datastore)

def authenticate(username, password):
    user = _datastore.get_user(username)

    if user and user.confirmed_at and verify_and_update_password(password, user):
        _log.info("%s authenticated successfully", username)
        _request_ctx_stack.top.current_user = user
        return user

    if not user:
        _log.warn("Authentication failed; unknown username %s", username)
    else:
        _log.warn("Authentication failed; invalid password for %s", username)

    if user and not user.confirmed_at:
        _log.warn("Account has not been confirmed!")


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
    """Encodes the payload and returns a flask response"""
    #TODO all bitmasks should NOT be the same and should be saved as an attribute of the role
    masked_roles = [dict(bitMask=2, title=role.name) for role in current_user.roles]
    return jsonify(dict(token=payload, roles=masked_roles, name=current_user.first_name))
