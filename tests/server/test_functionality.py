# -*- coding: utf-8 -*-
"""
    tests.test_functionality
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test basic login and registration functionality

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import pytest
from flask import url_for
import sure

from app.models.users import User
from tests.factories import UserFactory, RoleFactory

class TestLoggingIn:

    def test_jwt_log_in_returns_200_with_token(self, user, testapi):
        data = dict(username=user.email, password='myprecious')
        res = testapi.post_json(url_for('jwt'), data)
        assert res.status_code == 200
        assert 'token' in res.json

    def test_jwt_log_in_fails_when_user_has_no_roles(self, userWithNoRoles, testapi):
        data = dict(username=userWithNoRoles.email, password='myprecious')
        res = testapi.post_json(url_for('jwt'), data, expect_errors=True)
        assert res.status_code == 400

    # def test_log_in_returns_200_with_email_on_page(self, user, testapi):
    #     # Goes to homepage
    #     res = testapi.get("/")
    #     # Clicks Login link
    #     res = res.click("Login")
    #     # Fills out login form
    #     form = res.forms['login_form']
    #     form['email'] = user.email
    #     form['password'] = 'myprecious'
    #     # Submits
    #     res = form.submit().follow()
    #     assert res.status_code == 200
    #     assert user.email in res

    # def test_sees_login_link_on_log_out(self, user, testapi):
    #     res = testapi.get("/login", expect_errors=True)
    #     # Fills out login form on the login page
    #     form = res.forms['login_form']
    #     form['email'] = user.email
    #     form['password'] = 'myprecious'
    #     # Submits
    #     res = form.submit().follow()
    #     res = testapi.get(url_for('security.logout')).follow()
    #     # sees login link
    #     assert url_for('security.login') in res
    #
    # def test_sees_error_message_if_password_is_incorrect(self, user, testapi):
    #     # Goes to homepage
    #     res = testapi.get("/login")
    #     # Fills out login form, password incorrect
    #     form = res.forms['login_form']
    #     form['email'] = user.email
    #     form['password'] = 'wrong'
    #     # Submits
    #     res = form.submit()
    #     # sees error
    #     assert "Invalid password" in res
    #
    # def test_sees_error_message_if_username_doesnt_exist(self, user, testapi):
    #     # Goes to homepage
    #     res = testapi.get("/login")
    #     # Fills out login form with an unknown email
    #     form = res.forms['login_form']
    #     form['email'] = 'unknown'
    #     form['password'] = 'myprecious'
    #     # Submits
    #     res = form.submit()
    #     # sees error
    #     assert "user does not exist" in res

    # def test_auth_jwt_token_succeeds_with_logged_in_user_and_json_post(self, user, testapi):
    #     self.test_log_in_returns_200_with_email_on_page(user, testapi)
    #     resp = testapi.post_json("/auth/jwt/token", {})
    #     assert resp.status_code == 200
    #     assert 'token' in resp.json

    # def test_auth_jwt_token_fails_with_logged_in_user_and_non_json_post(self, user, testapi):
    #     self.test_log_in_returns_200_with_email_on_page(user, testapi)
    #     resp = testapi.post("/auth/jwt/token", {}, expect_errors=True)
    #     assert resp.status_code == 415

    # def test_auth_jwt_token_fails_without_logged_in_user(self, user, testapi):
    #     resp = testapi.post_json("/auth/jwt/token", {}, expect_errors=True)
    #     assert resp.status_code == 401


# class TestRegistering:
#
#     def test_can_register(self, user, testapi):
#         old_count = len(User.all())
#         # Goes to homepage
#         res = testapi.get("/")
#         # Clicks Create Account button
#         res = res.click("Login")
#         res = res.click("register")
#         # Fills out the form
#         form = res.forms["register_form"]
#         form['email'] = 'foo@bar.com'
#         form['password'] = 'secret'
#         form['password_confirm'] = 'secret'
#         # Submits
#         res = form.submit().follow()
#         assert res.status_code == 200
#         # A new user was created
#         assert len(User.all()) == old_count + 1
#
#     def test_sees_error_message_if_the_password_is_too_short(self, user, testapi):
#         # Goes to registration page
#         res = testapi.get(url_for("security.register"))
#         # Fills out registration form, but password is too short
#         form = res.forms["register_form"]
#         form['email'] = 'foo@bar.com'
#         form['password'] = 'short'
#         form['password_confirm'] = 'short'
#         # Submits
#         res = form.submit()
#         # sees error
#         assert "Password must be at least 6 characters" in res
#
#     def test_sees_error_message_if_passwords_dont_match(self, user, testapi):
#         # Goes to registration page
#         res = testapi.get(url_for("security.register"))
#         # Fills out form, but passwords don't match
#         form = res.forms["register_form"]
#         form['email'] = 'foobar'
#         form['email'] = 'foo@bar.com'
#         form['password'] = 'secret'
#         form['password_confirm'] = 'secrets'
#         # Submits
#         res = form.submit()
#         # sees error message
#         assert "Passwords do not match" in res
#
#     def test_sees_error_message_if_user_already_registered(self, user, testapi):
#         user = UserFactory(active=True)  # A registered user
#         user.save()
#         # Goes to registration page
#         res = testapi.get(url_for("security.register"))
#         # Fills out form, but username is already registered
#         form = res.forms["register_form"]
#         form['email'] = user.email
#         form['password'] = 'secret'
#         form['password_confirm'] = 'secret'
#         # Submits
#         res = form.submit()
#         # sees error
#         assert "is already associated with an account" in res
