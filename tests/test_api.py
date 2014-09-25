import unittest, sure, logging, tempfile, os, json
from datetime import datetime
import app as vitals
from app import Event, Source
from dougrain import Document
from tests import hal_loads

logger = logging.getLogger(__name__)

class ApiTest(unittest.TestCase):
	def setUp(self):
		"""Construct temporary database and test client for testing routing and responses"""
		self.db_fd, self.db_path = tempfile.mkstemp()
		vitals.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % self.db_path
		vitals.app.config['TESTING'] = True
		self.test_client = vitals.app.test_client()
		vitals.db.create_all()

	def tearDown(self):
		"""Removes temporary database at end of each test"""
		os.close(self.db_fd)
		os.unlink(self.db_path)


class EventListTest(ApiTest):
	"""Tests of api 'EventList' resource"""

	def test_link_relation_curie(self):
		"""Verify that Event resource has a link relation curie in HAL response"""
		resp = self.test_client.get('/api/events')
		doc = hal_loads(resp.data)
		curie_url = doc.links.curies['r'].url()
		curie_variables = doc.links.curies['r'].variables
		(curie_url).should.equal('/api/rels/')
		(curie_variables).should.equal(['rel'])

	def test_empty_events(self):
		"""
		Call to Event collection should contain link to self and be empty
		"""
		resp = self.test_client.get('/api/events')
		doc = hal_loads(resp.data)

		(resp.status_code).should.equal(200)
		(doc.properties['total']).should.equal(0)
		(doc.links['self'].url()).should.equal('/api/events?page=1')
		(doc.embedded.keys()).should.equal([])

	def test_single_event(self):
		"""
		Call to Event collection with single event
		"""
		event = Event('http://www.foo.com', 'Test', 'chicago', datetime.now())
		vitals.db.session.add(event)
		vitals.db.session.commit()

		resp = self.test_client.get('/api/events')
		doc = hal_loads(resp.data)

		(doc.embedded.keys()).should.equal(['r:event'])
		doc.embedded['r:event']

	def test_links(self):
		"""
		A large event collection should return links to navigate the collection 
		"""
		for x in range(100):
			event = Event('http://www.foo.com/%d' % x, 'Test%d' % x, 'chicago', datetime.now())
			vitals.db.session.add(event)
		vitals.db.session.commit()

		resp = self.test_client.get('/api/events')
		doc = hal_loads(resp.data)

		(doc.links['next'].url()).should.equal('/api/events?page=2')
		doc.links['last'].url().should.equal('/api/events?page=5')
		doc.links['first'].url().should.equal('/api/events?page=1')
		doc.links['self'].url().should.equal('/api/events?page=1')
		(doc.embedded.keys()).should.equal(['r:event'])
		doc.embedded['r:event']

	def test_bad_page(self):
		"""
		Page should not be able to be 0 or > num_pages
		"""
		for x in range(5):
			event = Event('http://www.foo.com/%d' % x, 'Test%d' % x, 'chicago', datetime.now())
			vitals.db.session.add(event)
		vitals.db.session.commit()

		resp = self.test_client.get('/api/events?page=0')
		(resp.status_code).should.equal(404)

		resp = self.test_client.get('/api/events?page=6')
		(resp.status_code).should.equal(404)

class SourceTest(ApiTest):
	"""Test of API 'Source' resource"""

	def test_link_relation_curie(self):
		"""Verify that resource has a link relation curie in HAL response"""
		resp = self.test_client.get('/api/sources')
		doc = hal_loads(resp.data)

		curie_url = doc.links.curies['r'].url()
		curie_variables = doc.links.curies['r'].variables
		(curie_url).should.equal('/api/rels/')
		(curie_variables).should.equal(['rel'])

	def test_empty_sources(self):
		"""
		Get all members of Sources collection and verify that it's an empty data set
		"""
		resp = self.test_client.get('/api/sources')
		doc = hal_loads(resp.data)

		(resp.status_code).should.equal(200)
		(doc.links['self'].url()).should.equal('/api/sources')
		(doc.embedded.keys()).should.equal([])
