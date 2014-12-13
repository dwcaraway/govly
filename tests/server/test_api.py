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
from tests.factories import UserFactory

@pytest.fixture
def user(db):
    return UserFactory(password='myprecious')

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

    def test_jwt_log_in_returns_200_with_token(self, user, testapi):
        data = dict(username=user.email, password='myprecious')
        resp = testapi.post_json('/auth', data)
        assert resp.status_code == 200
        assert 'token' in resp.json
        return resp.json['token']


class TestAPILoggingIn:

    def test_jwt_log_in_returns_200_with_token(self, user, testapi):
        data = dict(username=user.email, password='myprecious')
        resp = testapi.post_json('/auth', data)
        assert resp.status_code == 200
        assert 'token' in resp.json
        return resp.json['token']

    def test_secure_endpoint_fails_without_token(self, user, testapi):
        resp = testapi.get("/secure", expect_errors=True)
        assert resp.status_code == 401

    def test_secure_endpoint_succeeds_with_jwt_token(self, user, testapi):
        token = self.test_jwt_log_in_returns_200_with_token(user, testapi)
        resp = testapi.get("/secure", headers={
            "Authorization": "Bearer {token}".format(token=token),
        })
        assert resp.status_code == 200
        assert 'secret' in resp.json

    def test_secure_endpoint_fails_after_user_reset_secret(self, user, testapi):
        token = self.test_jwt_log_in_returns_200_with_token(user, testapi)
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

class TestLinkRelation:
    """Test of API 'LinkRelation' resource"""

    def test_list_all(self, testapi):
        """
        Get all members of Link Relations collection and verify that it's an empty data set
        """
        # url_for('v1.LinkRelationsView:index')

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

    def test_link_relation_curie(self, apidb, testapi):
        """Verify that resource has a link relation curie in HAL response"""
        resp = testapi.get(url_for('v1.OrganizationsView:index'))
        expected_template = url_for('v1.LinkRelationsView:index')+'/{rel}'
        resp.hal.links.curies['r'].template.should.equal(expected_template)

    def test_empty_organizations(self, apidb, testapi):
        """
        Get all members of Organization collection and verify that it's an empty data set
        """
        resp = testapi.get(url_for('v1.OrganizationsView:index'))
        doc = resp.hal
        doc.links['self'].url().should.equal(url_for('v1.OrganizationsView:index', page=1))
        doc.properties['total'].should.equal(0)
        doc.embedded.should.be.empty

    def test_single_organization(self, org, testapi):
        """
        Call to Organization collection with single organization
        """

        resp = testapi.get(url_for('v1.OrganizationsView:index'))
        doc = resp.hal

        #There should only be links
        doc.links['r:organization'].url().should.equal(url_for('v1.OrganizationsView:get', id=org.id))

        #Should not have 'first' and 'last' links
        doc.links.keys().shouldnot.contain('first')
        doc.links.keys().shouldnot.contain('last')
        doc.embedded.should.be.empty

    def test_large_business_collection(self, testapi, orgs):
        """
        Create a bunch of organizations and verify the links are correct
        """

        resp = testapi.get(url_for('v1.OrganizationsView:index'))
        doc = resp.hal

        doc.links.keys().shouldnot.contain('first')
        doc.links['last'].url().should.equal(url_for('v1.OrganizationsView:index', page=5))

    def test_get(self, testapi, org):
        """
        Get single organization
        """
        resp = testapi.get(url_for('v1.OrganizationsView:get', id=org.id))

        doc = resp.hal
        doc.links['r:organizations'].url().should.equal(url_for('v1.OrganizationsView:index', page=1))
