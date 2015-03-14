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

#@pytest.mark.usefixtures('apidb')
class TestAdminPanel:
    """Tests for the administrative panel"""

    def test_admin_role_required_to_login(self, admin_user):
        #TODO we need some admin panel tests!!!! accomplish right after we get initial users into system, Dave!
        #As of 13 March 2015
        pass

    # def test_unauthenticated_user_directed_to_login, user, testapp):
    #     res = testapp.get(url_for(''))
    #     # Fills out login form on the login page
    #     form = res.forms['login_form']
    #     form['email'] = user.email
    #     form['password'] = 'myprecious'
    #     # Submits
    #     res = form.submit().follow()
    #     res = testapp.get(url_for('security.logout')).follow()
    #     # sees login link
    #     assert url_for('security.login') in res
    #
    # def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
    #     # Goes to homepage
    #     res = testapp.get("/login")
    #     # Fills out login form, password incorrect
    #     form = res.forms['login_form']
    #     form['email'] = user.email
    #     form['password'] = 'wrong'
    #     # Submits
    #     res = form.submit()
    #     # sees error
    #     assert "Invalid password" in res


