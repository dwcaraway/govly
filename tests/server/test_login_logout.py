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

class TestLoggingIn:

    def test_jwt_log_in_returns_200_with_token(self, user, testapi):
        data = dict(username=user.email, password='myprecious')
        resp = testapi.post_json(url_for('jwt'), data)
        resp.status_code.should.equal(200)
        resp.json.should.contain('token')
        resp.json.should.contain('roles')
        resp.json.should.contain('name')
        return resp.json['token']

    def test_login_returns_id_in_token(self, user, testapi):
        token = self.test_jwt_log_in_returns_200_with_token(user, testapi)
        from flask_jwt import _default_decode_handler as d
        payload = d(token)
        user.id.should.equal(payload['user_id'])

    def test_login_records_login_information(self, user, testapi):
        last_login_at = user.last_login_at
        last_login_ip = user.last_login_ip
        current_login_at = user.current_login_at
        current_login_ip = user.current_login_ip

        token = self.test_jwt_log_in_returns_200_with_token(user, testapi)

        user.last_login_at.should.equal(current_login_at)
        user.last_login_ip.should.equal(current_login_ip)
        user.current_login_at.should_not.equal(current_login_at)
        user.current_login_ip.should_not.equal(current_login_ip)

    def test_secure_endpoint_fails_without_token(self, user, testapi):
        resp = testapi.get("/secure", expect_errors=True)
        assert resp.status_code == 401

    def test_secure_endpoint_succeeds_with_jwt_token(self, user, token, testapi):
        resp = testapi.get("/secure", headers={
            "Authorization": "Bearer {token}".format(token=token),
        })
        assert resp.status_code == 200
        assert 'secret' in resp.json

    def test_secure_endpoint_fails_after_user_reset_secret(self, user, token, testapi):
        resp = testapi.get("/secure", headers={
            "Authorization": "Bearer {token}".format(token=token),
        })
        assert resp.status_code == 200
        assert 'secret' in resp.json
        user.reset_secret()
        resp = testapi.get("/secure", headers={
            "Authorization": "Bearer {token}".format(token=token),
        }, expect_errors=True)
        assert resp.status_code == 400
        assert resp.json['error'] == 'Invalid JWT'
        assert resp.json['description'] == 'Invalid secret'

    def test_cors_allows_authorization_header(self, token, testapi):
        """Verify that cross origin CORS posts with Authorization header are allowed"""
        resp = testapi.options("/secure", headers={
            "Authorization": "Bearer {token}".format(token=token),
            'Access-Control-Request-Method': 'GET'
        })

        resp.headers.get('Access-Control-Allow-Origin').should.equal('*')
        resp.headers.get('Access-Control-Allow-Headers').should.contain('Content-Type')
        resp.headers.get('Access-Control-Allow-Headers').should.contain('Authorization')

class TestLoggingOut:

    def test_logout_requires_jwt_header(self, testapi):
        resp = testapi.get(url_for('v1.AuthView:logout'), expect_errors=True)
        assert resp.status_code == 401

    def test_logout_requires_valid_jwt(self, testapi):
        resp = testapi.get(url_for('v1.AuthView:logout'), headers={
            "Authorization": "Bearer {token}".format(token='nota.real.token'),
        }, expect_errors=True)
        assert resp.status_code == 400

    def test_logout_succeeds_with_valid_token(self, user, token, testapi):
        resp = testapi.get(url_for('v1.AuthView:logout'), headers={
            "Authorization": "Bearer {token}".format(token=token),
        }, expect_errors=True)
        resp.status_code.should.equal(200)

    def test_logout_resets_secret(self, user, token, testapi):
        original_secret = user.secret
        self.test_logout_succeeds_with_valid_token(user, token, testapi)
        user.secret.should_not.equal(original_secret)

