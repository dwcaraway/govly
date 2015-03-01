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
import sure

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

