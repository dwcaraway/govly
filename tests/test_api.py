import unittest
import logging
import tempfile
import os
from datetime import datetime

from app.model import db, Event, Organization, OrganizationSource, User
from tests import hal_loads
from app import create_application
import sure
import json
from app.config import TestingConfig
from flask import url_for

logger = logging.getLogger(__name__)

class ApiTest(unittest.TestCase):
    def setUp(self):
        """Construct temporary database and test client for testing routing and responses"""
        self.vitals = create_application(TestingConfig())
        self.vitals.testing = True
        self.test_client = self.vitals.test_client()

        #Push a context so that database knows what application to attach to
        self.ctx = self.vitals.test_request_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        """Removes temporary database at end of each test"""
        db.session.remove()
        db.drop_all()

        # os.close(self.db_fd)
        # os.unlink(self.db_path)

        #Remove the context so that we can create a new app and reassign the db
        self.ctx.pop()


class EndpointsTests(ApiTest):
    """Tests the root endpoint"""

    def test_endpoints(self):
        resp = self.test_client.get('/api/')
        doc = hal_loads(resp.data)

        resp.status_code.should.equal(200)
        doc.links['r:events'].url().should.equal('/api/events')
        doc.links['r:sources'].url().should.equal('/api/sources')
        doc.links['r:businesses'].url().should.equal('/api/businesses')


class EventListTest(ApiTest):
    """Tests of api 'EventList' resource"""

    def test_link_relation_curie(self):
        """Verify that Event resource has a link relation curie in HAL response"""
        resp = self.test_client.get('/api/events')
        doc = hal_loads(resp.data)
        curie_url = doc.links.curies['r'].url()
        curie_variables = doc.links.curies['r'].variables
        curie_url.should.equal('/api/rels/')
        curie_variables.should.equal(['rel'])

    def test_empty_events(self):
        """
        Call to Event collection should contain link to self and be empty
        """
        resp = self.test_client.get('/api/events')
        doc = hal_loads(resp.data)

        resp.status_code.should.equal(200)
        doc.properties['total'].should.equal(0)
        doc.links['self'].url().should.equal('/api/events?page=1')
        doc.embedded.keys().should.equal([])

    def test_single_event(self):
        """
        Call to Event collection with single event
        """
        event = Event('http://www.foo.com', 'Test', 'chicago', datetime.now())

        db.session.add(event)
        db.session.commit()

        resp = self.test_client.get('/api/events')
        doc = hal_loads(resp.data)

        doc.links['r:event'].url().should.equal('/api/events/%d' % event.id)



    def test_links(self):
        """
        A large event collection should return links to navigate the collection
        """
        for x in range(100):
            event = Event('http://www.foo.com/%d' % x, 'Test%d' % x, 'chicago', datetime.now())
            db.session.add(event)
            db.session.commit()

        resp = self.test_client.get('/api/events')
        doc = hal_loads(resp.data)

        doc.links['next'].url().should.equal('/api/events?page=2')
        doc.links['last'].url().should.equal('/api/events?page=5')
        doc.links.keys().shouldnot.contain('first')
        doc.links['self'].url().should.equal('/api/events?page=1')
        len(doc.links['r:event']).should.equal(20)
        doc.properties['total'].should.equal(100)
        doc.embedded.keys().should.equal([])

    def test_bad_page(self):
        """
        Page should not be able to be 0 or > num_pages
        """
        for x in range(5):
            event = Event('http://www.foo.com/%d' % x, 'Test%d' % x, 'chicago', datetime.now())
            db.session.add(event)
            db.session.commit()

        resp = self.test_client.get('/api/events?page=0')
        resp.status_code.should.equal(404)

        resp = self.test_client.get('/api/events?page=6')
        resp.status_code.should.equal(404)

    def test_create_event(self):
        """
        Create an event
        """
        resp = self.test_client.post('/api/events', data=dict())
        doc = hal_loads(resp.data)

        resp.status_code.should.equal(201)

        len(Event.query.all()).should.equal(1)

        doc.properties['id'].should.equal(Event.query.first().id)

class SourcesTest(ApiTest):
    """Test of API 'Sources' resource"""

    def test_link_relation_curie(self):
        """Verify that resource has a link relation curie in HAL response"""
        resp = self.test_client.get('/api/sources')
        doc = hal_loads(resp.data)

        curie_url = doc.links.curies['r'].url()
        curie_variables = doc.links.curies['r'].variables
        curie_url.should.equal('/api/rels/')
        curie_variables.should.equal(['rel'])

    def test_empty_sources(self):
        """
        Get all members of Sources collection and verify that it's an empty data set
        """
        resp = self.test_client.get('/api/sources')
        doc = hal_loads(resp.data)

        resp.status_code.should.equal(200)
        doc.links['self'].url().should.equal('/api/sources?page=1')
        doc.properties['total'].should.equal(0)
        doc.embedded.keys().should.equal([])

class SourceTest(ApiTest):
    def test_get(self):
        """
        Get single source
        """
        o = Organization(legalName='somename')
        src = OrganizationSource(spider_name='foo', data_url='http://www.foo.com', organization=o)

        db.session.add(o)
        db.session.add(src)
        db.session.commit()

        resp = self.test_client.get('/api/sources/%d'%src.id)
        resp.status_code.should.equal(200)

        doc = hal_loads(resp.data)
        doc.links['r:sources'].url().should.equal('/api/sources')
        doc.properties.should.equal({'data_url':'http://www.foo.com', 'organization_id':o.id, 'spider_name': 'foo', 'id':src.id})

class BusinessesTest(ApiTest):
    """Test of API 'Businesses' resource"""

    def test_link_relation_curie(self):
        """Verify that resource has a link relation curie in HAL response"""
        resp = self.test_client.get('/api/businesses')
        doc = hal_loads(resp.data)

        curie_url = doc.links.curies['r'].url()
        curie_variables = doc.links.curies['r'].variables
        curie_url.should.equal('/api/rels/')
        curie_variables.should.equal(['rel'])

    def test_empty_businesses(self):
        """
        Get all members of Businesses collection and verify that it's an empty data set
        """
        resp = self.test_client.get('/api/businesses')
        doc = hal_loads(resp.data)

        resp.status_code.should.equal(200)
        doc.links['self'].url().should.equal('/api/businesses?page=1')
        doc.properties['total'].should.equal(0)
        doc.embedded.keys().should.equal([])

    def test_single_business(self):
        """
        Call to Businesses collection with single event
        """
        biz = Organization(legalName='somename')

        db.session.add(biz)
        db.session.commit()

        resp = self.test_client.get('/api/businesses')
        doc = hal_loads(resp.data)

        #There should only be links
        doc.links['r:business'].url().should.equal('/api/businesses/%d' % biz.id)

        doc = hal_loads(resp.data)

        #Should not have 'first' and 'last' links
        doc.links.keys().shouldnot.contain('first')
        doc.links.keys().shouldnot.contain('last')
        doc.embedded.keys().should.equal([])

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

class BusinessTest(ApiTest):
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

class SecurityTest(ApiTest):

    def test_account_registration_creates_account(self):
        """
        Given that I am an unauthenticated user
        When I post an email and password to <r:signup url>
        Then I receive a HTTP 201 code indicating account creation
        """
        url = None
        with self.vitals.app_context():
            url = url_for('api.signup')

        data = {'email':'me@colliderproject.org', 'password':"bestpasswordever!"}
        headers = {'Content-Type': 'application/json'}

        resp = self.test_client.post(url, data=json.dumps(data), headers=headers)
        resp.status_code.should.equal(201)

        with self.vitals.app_context():
            User.query.all().should.have.length_of(1)
            db.user_datastore.get_user(data['email']).shouldnot.equal(None)

    def test_account_registration_sends_email(self):
        """
        Given that I am an unauthenticated user
        When I post an email and password to <r:signup url>
        Then I may not log in yet and
        I receive an email with a confirmation link
        """

        from contextlib import contextmanager
        from flask_security.signals import confirm_instructions_sent
        from flask_security.utils import login_instructions_sent

        @contextmanager
        def captured_emails(app):
            recorded = []
            def record(sender, user, **extra):
                recorded.append(user)
                confirm_instructions_sent.connect(record, app)
            try:
                yield recorded
            finally:
                confirm_instructions_sent.disconnect(record, app)

#        with captured_emails(self.vitals) as emails:

        with self.vitals.mail.record_messages() as outbox:
            url = None
            with self.vitals.app_context():
                url = url_for('api.signup')

            data = {'email':'me@colliderproject.org', 'password':"!bestpasswordever!"}
            headers = {'Content-Type': 'application/json'}

            resp = self.test_client.post(url, data=json.dumps(data), headers=headers)

            outbox.should.have.length_of(1)

#            emails.should.have.length_of(1)
#            emails[0].user.email.should.equal('me@colliderproject.org')

