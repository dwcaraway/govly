import unittest, sure, logging, tempfile, os, json
import app as vitals
from dougrain import Document

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


class EventTest(ApiTest):
	"""Tests of api 'Event' resource"""

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
		(doc.links['self'].url()).should.equal('/api/events')
		(doc.embedded.keys()).should.equal([])

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

class LinkRelationTest(ApiTest):
	"""Test of API 'LinkRelation' resource"""

	def test_empty_link_relations(self):
		"""
		Get all members of Link Relations collection and verify that it's an empty data set
		"""
		resp = self.test_client.get('/api/rels')
		doc = hal_loads(resp.data)

		(resp.status_code).should.equal(200)

def hal_loads(resp_str):
	"""Helper function that converts a string into a HAL object"""	
	return Document.from_object(json.loads(resp_str))
