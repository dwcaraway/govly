# -*- coding: utf-8 -*-
"""
    vitals.framework.utils
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import base64
import os

from flask import flash, current_app
from werkzeug.local import LocalProxy
from flask.ext.mail import Message
import uuid

_security = LocalProxy(lambda: current_app.extensions['security'])
_mail = LocalProxy(lambda: current_app.extensions['mail'])

def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)

def generate_salt():
    """Generate a random string used for salts and secret keys."""
    return base64.b64encode(os.urandom(32)).decode('utf-8')

def send_message(subject, sender, recipients, text_body, html_body):
    """Sends an email message out"""
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    _mail.send(msg)

def generate_invitation_token(user):
    """Generates a unique invitation token for the specified user.

    :param user: The user to work with
    """
    data = [user.id, str(uuid.uuid4())]
    return _security.invite_serializer.dumps(data)

