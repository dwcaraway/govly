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

class TestOpportunities:
    """Test of 'Opportunity' Resource"""

    def test_get(self, testapi, authHeader):
        """
        Get a collection with default parameters
        """
        resp = testapi.get(url_for('v1.OpportunitiesView:index'), headers=authHeader)

        resp.should_not.equal(None)
