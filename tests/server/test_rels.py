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

