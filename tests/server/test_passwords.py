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
from jsonschema import Draft4Validator
from flask_jwt import generate_token
from tests.factories import UserFactory, RoleFactory
from app.models.users import User
from app.framework.utils import generate_invitation_token
from bs4 import BeautifulSoup
from flask_security.utils import verify_password
import re
import sure

class TestPasswordChange:
    """Tests ability to perform a password change while authenticated"""

    def test_user_may_change_their_password(self, testapi, user, authHeader):
        oldPassword = 'myprecious'
        newPassword = 'foofoofoo'
        resp = testapi.post_json(url_for('v1.AuthView:change_password'), dict(new=newPassword, old=oldPassword),
                                 headers=authHeader)

        resp.status_code.should.equal(200)
        verify_password(newPassword, user.password).should.be.true

    def test_user_change_password_sends_email(self, testapi, user, mail, authHeader):
        with mail.record_messages() as outbox:
            self.test_user_may_change_their_password(testapi, user, authHeader)
            outbox.should.have.length_of(1)
            m = outbox[0]
            return m

class TestPasswordReset:
    """Tests ablity to generate a password reset email"""

    def test_user_may_request_password_reset_instructions(self, testapi, user, mail):
        with mail.record_messages() as outbox:
            resp = testapi.post_json(url_for('v1.AuthView:reset_request'), dict(email=user.email))
            resp.json.should.have.key('status').equal(200)
            outbox.should.have.length_of(1)
            m = outbox[0]
            return m

    def test_user_must_enter_a_valid_email_to_issue_reset_emaili(self, testapi, user, mail):

        resp = testapi.post_json(url_for('v1.AuthView:reset_request'), dict(email='notarealaddress@foo.me'), expect_errors=True)
        resp.status_code.should.equal(409)

    def test_email_address_not_on_record_does_not_generate_message(self, testapi, user, mail):
        with mail.record_messages() as outbox:
            testapi.post_json(url_for('v1.AuthView:reset_request'), dict(email='notarealaddress@foo.me'), expect_errors=True)
            outbox.should.have.length_of(0)

    def test_user_may_reset_password(self, testapi, user, mail):
        newPassword = 'foofoosecret'

        m = self.test_user_may_request_password_reset_instructions(testapi, user, mail)
        token = self.get_confirmation_token_from_email(m)

        testapi.post_json(url_for('v1.AuthView:update_password'), dict(password=newPassword, token=token))
        user.password.should.equal(newPassword)

    def test_reset_records_user_login(self, testapi, user, mail):
        #SEE 
        current_login_at = user.current_login_at
        last_login_at = user.last_login_at

        self.test_user_may_reset_password(testapi, user, mail)

        current_login_at.should_not.equal(user.current_login_at)
        last_login_at.should_not.equal(user.last_login_at)

    def get_confirmation_token_from_email(self, message):
        """Retrieves the confirmation link from the message"""
        soup = BeautifulSoup(message.html)
        return re.search('reset/(.*)', soup.a['href']).group(1)
