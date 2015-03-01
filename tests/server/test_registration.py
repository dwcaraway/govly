# -*- coding: utf-8 -*-
"""
    tests.test_api
    ~~~~~~~~~~~~~~

    Test API

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine, LLC

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import pytest
from flask import url_for
from flask_jwt import generate_token
from tests.factories import UserFactory, RoleFactory, InviteFactory
from app.models.users import User

from bs4 import BeautifulSoup
import re
import sure

class TestRegistration:
    """Test user registration via the API"""

    def test_register_data_invalid_email_generates_400(self, testapi, role, invite):
        data = {"firstName":"myFirstName", "lastName":"myLastName", "email":"notareal email address", "password":"supersecret", "token":invite.token}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data, expect_errors=True)

        resp.status_code.should.equal(400)
        resp.json['status'].should.equal(400)
        resp.json['message'].should.contain("is not a 'email'")

    def test_invite_is_required_to_register(self, testapi, role):
        data = {"firstName":"myFirstName", "lastName":"myLastName", "email":"notareal email address", "password":"supersecret"}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data, expect_errors=True)

        resp.status_code.should.equal(400)
        resp.json['status'].should.equal(400)
        resp.json['message'].should.contain("required arguments missing")

    def test_syntactically_valid_invite_is_required_to_register(self, testapi, role, invite):
        data = {"firstName":"myFirstName", "lastName":"myLastName", "email":"someone@somewhere.com", "password":"supersecret", "token":"badto"}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data, expect_errors=True)

        resp.status_code.should.equal(400)
        resp.json['status'].should.equal(400)
        resp.json['message'].should.contain("too short")

    def test_valid_invite_is_required_to_register(self, testapi, role, invite):
        data = {"firstName":"myFirstName", "lastName":"myLastName", "email":"someone@somewhere.com", "password":"supersecret", "token":"abadtokenhere"}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data, expect_errors=True)

        resp.status_code.should.equal(409)
        resp.json['status'].should.equal(409)
        resp.json['message'].should.contain("Invite is invalid")

    def test_register_user(self, apidb, testapi, role, invite):
        data = {"firstName":"myFirstName", "lastName":"myLastName", "email":"agent@secret.com", "password":"supersecret", "token":invite.token}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data)

        #test register user creates user but confirmed_at is not set
        u = User.query.filter_by(email=data['email']).first()

        from flask_security.utils import verify_and_update_password
        verify_and_update_password(user=u, password='supersecret').should_not.be.none
        u.confirmed_at.should.be.none

        return resp

    def test_register_user_assigns_user_role(self, apidb, testapi, role, invite):
        resp = self.test_register_user(apidb, testapi, role, invite=invite)
        resp.json['user']['roles'].should.have.length_of(1)

        u = User.first(email='agent@secret.com')
        u.roles.should.have.length_of(1)
        u.roles.should.contain(role)

    def test_register_user_returns_201(self, apidb, testapi, role, invite):
        resp = self.test_register_user(apidb, testapi, role, invite=invite)
        resp.status_code.should.equal(201)
        resp.json['status'].should.equal(201)
        resp.json['message'].should.contain("A confirmation email has been sent to agent@secret.com")
        resp.json['user'].should_not.be.none
        resp.json['user']['token'].should_not.be.none

    def test_register_user_sends_confirmation_email(self, apidb, testapi, mail, role, invite):
        with mail.record_messages() as outbox:
            self.test_register_user(apidb, testapi, role, invite)
            outbox.should.have.length_of(1)
            m = outbox[0]
            return m

    def test_registered_but_unconfirmed_user_may_login(self, apidb, testapi, role, invite):
        self.test_register_user(apidb, testapi, role, invite)
        u = User.query.filter_by(email='agent@secret.com').first()
        resp = testapi.post_json(url_for('jwt'), dict(username=u.email, password='supersecret'))
        resp.status_code.should.equal(200)

    def test_user_may_not_register_twice(self, apidb, testapi, user, invite):
        data = {'email': user.email, 'password':'doesnt_matter', 'firstName':'joe', 'lastName':'bob', "token":invite.token}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data, expect_errors=True)
        resp.status_code.should.equal(409)
        resp.json['status'].should.equal(409)
        resp.json['message'].should.contain('email already exists')

    def test_invite_may_be_used_only_once(self, apidb, testapi, role, invite):
        self.test_register_user(apidb=apidb, testapi=testapi, role=role, invite=invite)

        # This second registration attempt will try to use the same token. It should NOT be able to succeed.
        userData2 = {'email': "user2@me.com", 'password':'doesnt_matter', 'firstName':'jimminey', 'lastName':'jimminy', "token":invite.token}

        resp = testapi.post_json(url_for('v1.AuthView:register_user'), userData2, expect_errors=True)
        resp.status_code.should.equal(409)
        resp.json['status'].should.equal(409)
        resp.json['message'].should.contain('Invite already used')

    def test_confirm_user(self, apidb, testapi, mail, role, invite):
        m = self.test_register_user_sends_confirmation_email(apidb, testapi, mail, role, invite=invite)

        token = self.get_confirmation_token_from_email(m)
        href = url_for('v1.AuthView:confirm_email')

        resp = testapi.post_json(href, dict(token=token))

        # confirmed user should receive a login credential set
        resp.status_code.should.equal(200)
        resp.json.get('user').should_not.be.none

    def test_confirm_user_with_bad_token_409(self, apidb, testapi, mail, role, invite):
        m = self.test_register_user_sends_confirmation_email(apidb, testapi, mail, role, invite=invite)
        href = url_for('v1.AuthView:confirm_email')
        resp = testapi.post_json(href, dict(token='notarealtoken'), expect_errors=True)
        resp.status_code.should.equal(409)
        resp.json['status'].should.equal(409)
        resp.json['message'].should.contain('Invalid')

    def test_user_may_not_confirm_twice(self, apidb, testapi, mail, role, invite):
        m = self.test_register_user_sends_confirmation_email(apidb, testapi, mail, role, invite=invite)

        token = self.get_confirmation_token_from_email(m)
        href = url_for('v1.AuthView:confirm_email')

        testapi.post_json(href, dict(token=token))
        resp2 = testapi.post_json(href, dict(token=token), expect_errors=True)

        resp2.status_code.should.equal(409)

    def test_user_may_not_use_expired_token(self, apidb, testapi, mail):
        #Token used via itsdangerous.URLSafeTimedSerializer
        old_token = {'secret':'super secret', 'salt':'salty', 'token':'ImZvbyI.B4ovjQ.UAh0LfwlwReM9_FTughkAHpvxkQ'}
        resp = testapi.post_json(url_for('v1.AuthView:confirm_email'), dict(token='notarealtoken'), expect_errors=True)

    def get_confirmation_token_from_email(self, message):

        """Retrieves the confirmation link from the message"""

        soup = BeautifulSoup(message.html)
        return re.search('token=(.*)', soup.a['href']).group(1)

