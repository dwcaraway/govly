# -*- coding: utf-8 -*-
"""
    vitals.api.v1.orgs
    ~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from flask.ext.restful import reqparse
from flask.ext.classy import route
from app.api.base import BaseView, secure_endpoint
from app.models.users import User, Invite
from app.framework.utils import generate_invitation_token, send_message
from flask import render_template
from flask_jwt import current_user
from werkzeug.exceptions import NotFound, Unauthorized, NotImplemented, Conflict
from marshmallow import Schema, fields
from urlparse import urljoin
from flask import current_app, url_for
from sqlalchemy.exc import IntegrityError

from dougrain import Builder

class InviteSchema(Schema):
    id = fields.Integer()
    invitee_email = fields.Email()
    invitor_id = fields.Integer()
    invitee_id = fields.Integer()
    token = fields.String()

user_parser = reqparse.RequestParser()
user_parser.add_argument('q', type=str, help='Free-text search string', default="")

user_invitation_post_parser = reqparse.RequestParser()
user_invitation_post_parser.add_argument('email', type=str, location='json', help="The email address to send the invite to", required=True)

class UsersView(BaseView):
    """A complete Flask-Classy-based Users API resource."""

    @secure_endpoint()
    def index(self):
        """Returns a Collection of Users"""

        raise NotImplemented('TODO')

    @secure_endpoint()
    def get(self, id):
        """Returns a specific of User"""

        raise NotImplemented('TODO')

    @secure_endpoint()
    @route('<userid>/invitations/<inviteid>')
    def get_invitation(self, userid, inviteid):
        """Returns a user's collection of Invitations"""
        #TODO replace boilerplate with decorator
        user = User.get(id)

        if not user:
            raise NotFound()

        if current_user.id != user.id:
            raise Unauthorized('user id does not match requesting user id')
        #END boilerplate

        raise NotImplemented('TODO')

    @secure_endpoint()
    @route('<id>/invitations', methods=['POST'])
    def post_invitation(self, id):
        """Create a new invitation"""

        #TODO replace boilerplate with decorator
        user = User.get(id)

        if not user:
            raise NotFound()

        if current_user.id != user.id:
            raise Unauthorized('user id does not match requesting user id')
        #END boilerplate

        if len(user.invitations) >= current_app.config.get('MAX_INVITES'):
            raise Conflict("Maximum invitations reached")

        args = user_invitation_post_parser.parse_args()
        email = args.get('email')
        token = generate_invitation_token(user)

        try:
            invite = Invite.create(invitor_id=id, invitee_email=email, token=token)
        except IntegrityError as e:
            raise Conflict('%s has already been invited.' % email)

        invite_link = urljoin(current_app.config['CLIENT_DOMAIN'], '/#/register?token='+token)

        #TODO this mail send should be performed asynchronously using celery, see issue #88850472
        send_message(
            subject="You've been given early access to FogMine",
            sender="do-not-reply@fogmine.com",
            recipients = [user.email],
            html_body=render_template('email/invite.html', user=user, confirmation_link=invite_link),
            text_body=render_template('email/invite.txt', user=user, confirmation_link=invite_link)
        )

        schema = InviteSchema()
        jsonSerializableInvite = schema.dump(invite)[0]

        b = Builder(href=url_for('v1.UsersView:get_invitation', userid=id, inviteid=invite.id))\
            .add_curie('r', url_for('v1.LinkRelationsView:index')+"/{rel}")

        #TODO is there a simpler way to just add the whole dict here?
        for key, value in jsonSerializableInvite.iteritems():
            b.set_property(key, value)

        return b.o, 201
