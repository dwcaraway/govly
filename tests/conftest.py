# -*- coding: utf-8 -*-
"""
    tests.conftest
    ~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
import pytest
from webtest import TestApp

from app import api
from app.framework.sql import db as _db
from .settings import TestingConfig
from .apis import classy_api
from .factories import UserFactory, OrganizationFactory, RoleFactory, InviteFactory
from app.models.sam import *
from flask_jwt import generate_token
from webtest import TestResponse
from dougrain import Document
from app.framework.utils import generate_invitation_token

#monkey patch the TestResponse to return a HAL dougrain object
def hal(self):
        """
        Return the response as a JSON response.  You must have `simplejson
        <http://goo.gl/B9g6s>`_ installed to use this, or be using a Python
        version with the json module.

        The content type must be one of json type to use this.
        """
        if not self.content_type.endswith(('+json', '/json')):
            raise AttributeError(
                "Not a JSON response body (content-type: %s)"
                % self.content_type)
        return Document.from_string(self.testbody)

TestResponse.hal = property(hal)

@pytest.yield_fixture(scope='function')
def apiapp(request):
    _app = api.create_app(TestingConfig)
    classy_api(_app)
    with _app.test_request_context():
        yield _app

@pytest.fixture(scope='function')
def testapi(apiapp):
    """A Webtest app."""
    return TestApp(apiapp)

@pytest.yield_fixture(scope='function')
def apidb(apiapp):
    _db.app = apiapp
    with apiapp.app_context():
        _db.create_all()
    yield _db
    _db.drop_all()

@pytest.fixture
def user(apidb):
    return UserFactory()

@pytest.fixture
def org(apidb):
    return OrganizationFactory()

@pytest.fixture
def orgs(apidb):
    return OrganizationFactory.create_batch(size=100)

@pytest.fixture
def role(apidb):
    return RoleFactory()

@pytest.fixture
def user(role):
    u = UserFactory(password='myprecious')
    u.roles = [role] #Add a role
    u.save()

    return u

@pytest.fixture
def userNotSaved(role):
    """Build a user instance but don't save to database"""
    u = UserFactory.build(password='myprecious')
    return u

@pytest.fixture
def token(user):
    """Returns a JWT"""
    return generate_token(user)

@pytest.fixture
def authHeader(token):
    return dict(Authorization="Bearer {token}".format(token=token))

@pytest.fixture
def mail(apiapp):
    return apiapp.extensions['mail']

@pytest.fixture
def invite_token(user):
    return generate_invitation_token(user)

@pytest.fixture
def invite():
    return InviteFactory()

@pytest.fixture
def userWithNoRoles(role):
    return UserFactory(password='myprecious')