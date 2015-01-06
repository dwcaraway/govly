# -*- coding: utf-8 -*-
"""
    tests.test_api
    ~~~~~~~~~~~~~~

    Test API

    :author: 18F
    :copyright: © 2014-2015, 18F
    :license: CC0 Public Domain License, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import pytest
from flask import url_for
from jsonschema import Draft4Validator
from flask_jwt import generate_token
from tests.factories import UserFactory
from app.models.users import User
from bs4 import BeautifulSoup
import re

@pytest.fixture
def user(apidb):
    return UserFactory(password='myprecious')

@pytest.fixture
def token(user):
    return generate_token(user)

@pytest.fixture
def mail(apiapp):
    return apiapp.extensions['mail']

class TestAPI:
    """
    Tests both Flask-Classy and Flask-RESTful based APIs.  The `testapi` fixture
    will test each test function twice: `api_app0`==Classy, `api_app1`==RESTful.
    """

    def test_not_found(self, testapi):
        resp = testapi.get("/some-path-that-does-not-exist", expect_errors=True)
        assert resp.status_code == 404
        assert resp.json['status'] == 404
        assert 'Not Found' in resp.json['message']

    def test_not_found_with_envelope(self, testapi):
        resp = testapi.get("/non-existent-path?envelope=true", expect_errors=True)
        assert resp.status_code == 200
        assert resp.json['status'] == 404
        assert 'Not Found' in resp.json['data']['message']

    def test_not_found_with_callback(self, testapi):
        resp = testapi.get("/non-existent-path?callback=myfunc", expect_errors=True)
        assert resp.status_code == 200
        assert resp.json['status'] == 404
        assert 'Not Found' in resp.json['data']['message']

    def test_root_index(self, testapi):
        resp = testapi.get('/')
        resp.hal.links.should_not.be.empty

    def test_rel_index(self, testapi):
        resp = testapi.get("/rels")
        resp.json.should_not.be.empty

    def test_rel_index_is_valid_json_schema(self, testapi):
        resp = testapi.get("/rels")

        for schema in resp.json.itervalues():
            schema_errors = Draft4Validator.check_schema(schema)
            schema_errors.should.be.none

class TestLoggingIn:

    def test_jwt_log_in_returns_200_with_token(self, user, testapi):
        data = dict(username=user.email, password='myprecious')
        resp = testapi.post_json(url_for('jwt'), data)
        assert resp.status_code == 200
        assert 'token' in resp.json
        return resp.json['token']

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

class TestRegistration:
    """Test user registration via the API"""

    def test_register_data_invalid_email_generates_400(self, testapi):
        data = {"email":"notareal email address", "password":"supersecret"}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data, expect_errors=True)

        resp.status_code.should.equal(400)
        resp.json['status'].should.equal(400)
        resp.json['message'].should.contain("is not a 'email'")

    def test_register_user(self, apidb, testapi):
        data = {"email":"agent@secret.com", "password":"supersecret"}
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), data)

        #test register user creates user but confirmed_at is not set
        u = User.query.filter_by(email='agent@secret.com').first()

        from flask_security.utils import verify_and_update_password
        verify_and_update_password(user=u, password='supersecret').should_not.be.none
        u.confirmed_at.should.be.none

        return resp

    def test_register_user_returns_201(self, apidb, testapi):
        resp = self.test_register_user(apidb, testapi)
        resp.status_code.should.equal(201)
        resp.json['status'].should.equal(201)
        resp.json['message'].should.contain("A confirmation email has been sent.")

    def test_register_user_sends_confirmation_email(self, apidb, testapi, mail):
        with mail.record_messages() as outbox:
            self.test_register_user(apidb, testapi)
            outbox.should.have.length_of(1)
            m = outbox[0]
            return m

    def test_registered_but_unconfirmed_user_can_not_login(self, apidb, testapi):
        self.test_register_user(apidb, testapi)
        u = User.query.filter_by(email='agent@secret.com').first()
        resp = testapi.post_json(url_for('jwt'), dict(username=u.email, password='supersecret'), expect_errors=True)
        resp.status_code.should.equal(400)

        resp.json['status_code'].should.equal(400)
        resp.json['description'].should.equal('Invalid credentials')
        resp.json['error'].should.equal('Bad Request')


    def test_user_may_not_register_twice(self, apidb, testapi, user):
        resp = testapi.post_json(url_for('v1.AuthView:register_user'), dict(email=user.email, password='doesnt_matter'), expect_errors=True)
        resp.status_code.should.equal(409)
        resp.json['status'].should.equal(409)
        resp.json['message'].should.contain('email already exists')


    def test_confirm_user(self, apidb, testapi, mail):
        m = self.test_register_user_sends_confirmation_email(apidb, testapi, mail)

        href = self.get_confirmation_link_from_email(m)
        resp = testapi.get(href)

        # confirmed user should receive a token
        resp.status_code.should.equal(200)
        resp.json.get('token').should_not.be.none

    def test_confirm_user_with_bad_token_409(self, apidb, testapi, mail):
        m = self.test_register_user_sends_confirmation_email(apidb, testapi, mail)
        resp = testapi.get(url_for('v1.AuthView:confirm_email', token='notarealtoken'), expect_errors=True)
        resp.status_code.should.equal(409)
        resp.json['status'].should.equal(409)
        resp.json['message'].should.contain('Invalid')

    def test_user_may_not_confirm_twice(self, apidb, testapi, mail):
        m = self.test_register_user_sends_confirmation_email(apidb, testapi, mail)

        href = self.get_confirmation_link_from_email(m)
        resp1 = testapi.get(href)
        resp2 = testapi.get(href, expect_errors=True)

        resp2.status_code.should.equal(409)

    def test_user_may_not_use_expired_token(self, apidb, testapi, mail):
        #Token used via itsdangerous.URLSafeTimedSerializer
        old_token = {'secret':'super secret', 'salt':'salty', 'token':'ImZvbyI.B4ovjQ.UAh0LfwlwReM9_FTughkAHpvxkQ'}
        resp = testapi.get(url_for('v1.AuthView:confirm_email', token='notarealtoken'), expect_errors=True)

    def get_confirmation_link_from_email(self, message):

        """Retrieves the confirmation link from the message"""

        soup = BeautifulSoup(message.html)
        token = re.search('token=(.*)', soup.a['href']).group(1)
        return url_for('v1.AuthView:confirm_email', token=token)


class TestLinkRelation:
    """Test of API 'LinkRelation' resource"""

    def test_list_all(self, testapi):
        """
        Get all members of Link Relations collection and verify that it's an empty data set
        """
        resp = testapi.get(url_for('v1.LinkRelationsView:index'))
        resp.status_code.should.equal(200)
        len(resp.json.keys()).should.be.greater_than(1)

    def test_select_all(self, testapi):
        """
        Select all link relations and check them for valid JSON schema.
        """
        for rel_id in testapi.get(url_for('v1.LinkRelationsView:index')).json.keys():
            resp = testapi.get(url_for('v1.LinkRelationsView:get',id=rel_id))
            Draft4Validator.check_schema(resp.json).should.be(None)

    def test_rel_not_found(self, testapi):
        """Expect error object and message if rel not found"""
        resp = testapi.get(url_for('v1.LinkRelationsView:get',id='badrelname'), expect_errors=True)

        resp.status_code.should.equal(404)
        resp.json['message'].should.equal("Not Found")
        resp.json['status'].should.equal(404)

class TestOrganizations:
    """Test of 'Organization' resource"""

    def test_link_relation_curie(self, apidb, token, testapi):
        """Verify that resource has a link relation curie in HAL response"""
        resp = testapi.get(url_for('v1.OrganizationsView:index'), headers={
            "Authorization": "Bearer {token}".format(token=token),
        })
        expected_template = url_for('v1.LinkRelationsView:index')+'/{rel}'
        resp.hal.links.curies['r'].template.should.equal(expected_template)

    def test_empty_organizations(self, apidb, token, testapi):
        """
        Get all members of Organization collection and verify that it's an empty data set
        """
        resp = testapi.get(url_for('v1.OrganizationsView:index'), headers={
            "Authorization": "Bearer {token}".format(token=token),
        })
        doc = resp.hal
        doc.links['self'].url().should.equal(url_for('v1.OrganizationsView:index', page=1))
        doc.properties['total'].should.equal(0)
        doc.embedded.should.be.empty

    def test_single_organization(self, org, token, testapi):
        """
        Call to Organization collection with single organization
        """

        resp = testapi.get(url_for('v1.OrganizationsView:index'), headers={
            "Authorization": "Bearer {token}".format(token=token),
        })
        doc = resp.hal

        #There should only be links
        doc.links['r:organization'].url().should.equal(url_for('v1.OrganizationsView:get', id=org.id))

        #Should not have 'first' and 'last' links
        doc.links.keys().shouldnot.contain('first')
        doc.links.keys().shouldnot.contain('last')
        doc.embedded.should.be.empty

    def test_large_business_collection(self, testapi, token, orgs):
        """
        Create a bunch of organizations and verify the links are correct
        """

        resp = testapi.get(url_for('v1.OrganizationsView:index'), headers={
            "Authorization": "Bearer {token}".format(token=token),
        })
        doc = resp.hal

        doc.links.keys().shouldnot.contain('first')
        doc.links['last'].url().should.equal(url_for('v1.OrganizationsView:index', page=5))

    def test_get(self, testapi, org, token):
        """
        Get single organization
        """
        resp = testapi.get(url_for('v1.OrganizationsView:get', id=org.id), headers={
            "Authorization": "Bearer {token}".format(token=token),
        })

        doc = resp.hal
        doc.links['r:organizations'].url().should.equal(url_for('v1.OrganizationsView:index', page=1))
