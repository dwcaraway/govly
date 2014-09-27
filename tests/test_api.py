import unittest
import logging
import tempfile
import os
from datetime import datetime

from app.model import db, Event, Business
from tests import hal_loads
from app import create_application


logger = logging.getLogger(__name__)

class ApiTest(unittest.TestCase):
    def setUp(self):
        """Construct temporary database and test client for testing routing and responses"""
        self.db_fd, self.db_path = tempfile.mkstemp()

        config = {
        'SQLALCHEMY_DATABASE_URI':'sqlite:///%s' % self.db_path,
        'TESTING': True
        }

        self.vitals = create_application(config)
        self.test_client = self.vitals.test_client()

        #Push a context so that database knows what application to attach to
        self.ctx = self.vitals.test_request_context()
        self.ctx.push()

    def tearDown(self):
        """Removes temporary database at end of each test"""
        db.session.remove()
        db.drop_all()

        os.close(self.db_fd)
        os.unlink(self.db_path)

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
        doc.links['first'].url().should.equal('/api/events?page=1')
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

class SourceTest(ApiTest):
    """Test of API 'Source' resource"""

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
        doc.links['self'].url().should.equal('/api/sources')
        doc.embedded.keys().should.equal([])

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
        biz = Business()

        db.session.add(biz)
        db.session.commit()

        resp = self.test_client.get('/api/businesses')
        doc = hal_loads(resp.data)

        doc.embedded.keys().should.equal([])

class BusinessTest(ApiTest):
    def test_get(self):
        """
        Get single business
        """
        biz = Business(name='bar')

        db.session.add(biz)
        db.session.commit()

        resp = self.test_client.get('/api/businesses/%d'%biz.id)
        resp.status_code.should.equal(200)

        doc = hal_loads(resp.data)
        doc.links['r:events'].url().should.equal('/api/businesses?page=1')
        doc.properties.should.equal({'id':biz.id})
