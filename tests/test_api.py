import unittest
import logging
from datetime import datetime
import json

from flask import url_for

from app.framework.sql  import db
from app.models.users import User
from app.models.model import Organization, OrganizationSource
from tests import hal_loads
from .settings import TestingConfig
logger = logging.getLogger(__name__)

class BusinessesTest:
    """Test of API 'Businesses' resource"""





    def test_large_business_collection(self):
        """
        Create a bunch of businesses and verify the links are correct
        """
        for i in range(100):
            db.session.add(Organization(legalName='somename'))
        db.session.commit()

        resp = self.test_client.get('/api/businesses')
        doc = hal_loads(resp.data)

        doc.links.keys().shouldnot.contain('first')
        doc.links['last'].url().should.equal('/api/businesses?page=5')

    def test_search_finds_by_name(self):
        """
        Perform free text search for businesses using the q parameter.
        We first create a business, then we query for it where the match
        is in the name.
        """

        b = Organization(legalName="mr. bill")
        db.session.add(b)

        s = OrganizationSource(spider_name='testsrc', data_url='http://www.foo.com')
        s.organization = b

        db.session.add(s)
        db.session.commit()

        #Now
        resp = self.test_client.get('/api/businesses?q=bill')

        doc = hal_loads(resp.data)
        doc.links['r:business'].url().should.equal('/api/businesses/1')

class BusinessTest:
    def test_get(self):
        """
        Get single business
        """
        biz = Organization(legalName='somename')

        db.session.add(biz)
        db.session.commit()

        resp = self.test_client.get('/api/businesses/%d'%biz.id)
        resp.status_code.should.equal(200)

        doc = hal_loads(resp.data)
        doc.links['r:businesses'].url().should.equal('/api/businesses?page=1')
        doc.properties.should.equal({'id':biz.id, 'legalName':'somename','created_on':biz.created_on.isoformat(), 'updated_on': biz.updated_on.isoformat()})

# class SecurityTest(ApiTest):
#
#     def test_account_registration_creates_account(self):
#         """
#         Given that I am an unauthenticated user
#         When I post an email and password to <r:signup url>
#         Then I receive a HTTP 201 code indicating account creation
#         """
#         url = None
#         with self.vitals.app_context():
#             url = url_for('api.signup')
#
#         data = {'email':'me@colliderproject.org', 'password':"bestpasswordever!"}
#         headers = {'Content-Type': 'application/json'}
#
#         resp = self.test_client.post(url, data=json.dumps(data), headers=headers)
#         resp.status_code.should.equal(201)
#
#         with self.vitals.app_context():
#             User.query.all().should.have.length_of(1)
#             db.user_datastore.get_user(data['email']).shouldnot.equal(None)
#
#     def test_account_registration_sends_email(self):
#         """
#         Given that I am an unauthenticated user
#         When I post an email and password to <r:signup url>
#         Then I may not log in yet and
#         I receive an email with a confirmation link
#         """
#
#         from contextlib import contextmanager
#         from flask_security.signals import confirm_instructions_sent
#
#         @contextmanager
#         def captured_emails(app):
#             recorded = []
#             def record(sender, user, **extra):
#                 recorded.append(user)
#                 confirm_instructions_sent.connect(record, app)
#             try:
#                 yield recorded
#             finally:
#                 confirm_instructions_sent.disconnect(record, app)
#
# #        with captured_emails(self.vitals) as emails:
#
#         with self.vitals.mail.record_messages() as outbox:
#             url = None
#             with self.vitals.app_context():
#                 url = url_for('api.signup')
#
#             data = {'email':'me@colliderproject.org', 'password':"!bestpasswordever!"}
#             headers = {'Content-Type': 'application/json'}
#
#             resp = self.test_client.post(url, data=json.dumps(data), headers=headers)
#
#             outbox.should.have.length_of(1)
#
# #            emails.should.have.length_of(1)
# #            emails[0].user.email.should.equal('me@colliderproject.org')

