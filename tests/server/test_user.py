# -*- coding: utf-8 -*-
import datetime as dt
import pytest

from flask.ext.security.utils import verify_password

from flask import url_for

from app.models.users import User, Role
from tests.factories import UserFactory, InviteFactory
import sure
from bs4 import BeautifulSoup
import re

@pytest.mark.usefixtures('apidb')
class TestUser:

    def test_get(self, user):
        retrieved = User.get(user.id)
        assert retrieved == user

    def test_reset_secret(self, user):
        old_secret = user.secret
        user.reset_secret()
        assert old_secret != user.secret
        user = User.get(user.id)
        assert old_secret != user.secret

    def test_created_at_defaults_to_datetime(self, user):
        assert user.active
        assert bool(user.confirmed_at)
        assert bool(user.last_login_at)
        assert bool(user.current_login_at)
        assert isinstance(user.confirmed_at, dt.datetime)
        assert isinstance(user.last_login_at, dt.datetime)
        assert isinstance(user.current_login_at, dt.datetime)
        assert isinstance(user.secret, basestring)

    def test_password_is_nullable(self):
        user = User(email='foo@bar.com', first_name="foo", last_name="bar")
        user.save()
        assert user.password is None

    def test_factory(self):
        user = UserFactory()
        assert bool(user.email)
        assert bool(user.confirmed_at)
        assert user.active is True
        assert verify_password('password', user.password)

    def test_roles(self):
        role = Role(name='admin')
        role.save()
        u = UserFactory()
        u.roles.append(role)
        u.save()
        assert role in u.roles

    def test_404_if_user_id_for_invitation_doesnt_exist(self, testapi, authHeader):
        bad_user_id=234234980
        resp = testapi.post_json(url_for('v1.UsersView:post_invitation', id=bad_user_id),
                                 dict(email='someemail@foo.com'), headers=authHeader, expect_errors=True)
        resp.status_code.should.equal(404)

    def test_401_if_not_self(self, user, testapi, role, authHeader):
        """A user should not be able to access another user's profile and/or edit it"""
        another_user = UserFactory(password='myprecious')
        another_user.roles = [role]  # Add a role
        another_user.save()

        resp = testapi.post_json(url_for('v1.UsersView:post_invitation', id=another_user.id),
                                 dict(email='someemail@foo.com'), headers=authHeader, expect_errors=True)
        resp.status_code.should.equal(401)

    def test_create_an_invitation(self, testapi, user, authHeader):
        invitee_email = 'someluckydog@somewhere.com'

        resp = testapi.post_json(url_for('v1.UsersView:post_invitation', id=user.id),
                                 dict(email=invitee_email), headers=authHeader)
        resp.status_code.should.equal(201)

        doc = resp.hal

        #TODO
        # doc.links['self'].url().should.equal(url_for('v1.UsersView:index', page=1))
        doc.properties.keys().should.contain('id')
        doc.properties.keys().should.contain('invitee_email')

    def test_create_invitation_sends_message(self, testapi, mail, user, authHeader):
        with mail.record_messages() as outbox:
            self.test_create_an_invitation(testapi=testapi, user=user, authHeader=authHeader)
            outbox.should.have.length_of(1)
            m = outbox[0]
            return m

    def test_create_invitation_message_has_link(self, testapi, mail, user, authHeader):
        m = self.test_create_invitation_sends_message(testapi=testapi, mail=mail, user=user, authHeader=authHeader)
        token = get_confirmation_token_from_email(m)
        user.invitations[0].token.should.equal(token)

    def test_user_may_issue_up_to_5_invites(self, testapi, user, authHeader):
        tokens = InviteFactory.create_batch(size=5, invitor=user)
        resp = testapi.post_json(url_for('v1.UsersView:post_invitation', id=user.id),
                                 dict(email='doesnt@matter.co'), headers=authHeader, expect_errors=True)

        resp.status_code.should.equal(409)

    def test_user_may_not_invite_same_email_more_than_once(self, testapi, role, user, authHeader):
        email_to_invite = 'someemail@foo.com'

        from flask_jwt import generate_token

        another_user = UserFactory(password='myprecious')
        another_user.roles = [role]  # Add a role
        another_user.save()

        another_user_authheaders = dict(Authorization="Bearer {token}".format(token=generate_token(another_user)))

        resp = testapi.post_json(url_for('v1.UsersView:post_invitation', id=user.id),
                                 dict(email=email_to_invite), headers=authHeader)
        resp.status_code.should.equal(201)

        #Have another user also try to invite the same email address
        resp = testapi.post_json(url_for('v1.UsersView:post_invitation', id=another_user.id),
                         dict(email=email_to_invite), headers=another_user_authheaders, expect_errors=True)

        resp.status_code.should.equal(409)

def get_confirmation_token_from_email(message):

    """Retrieves the confirmation link from the message"""

    soup = BeautifulSoup(message.html)
    return re.search('token=(.*)', soup.a['href']).group(1)