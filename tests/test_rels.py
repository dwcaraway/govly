import unittest, sure, logging, tempfile, os, json
from app import create_application
from dougrain import Document
from jsonschema import Draft4Validator

logger = logging.getLogger(__name__)

class LinkRelationTest(unittest.TestCase):
	"""Test of API 'LinkRelation' resource"""

	def setUp(self):
		"""Construct temporary database and test client for testing routing and responses"""
		self.db_fd, self.db_path = tempfile.mkstemp()
		config = {
		'SQLALCHEMY_DATABASE_URI':'sqlite:///%s' % self.db_path,
		'TESTING': True
		}
		self.vitals = create_application(config)
		self.test_client = self.vitals.test_client()

	def tearDown(self):
		"""Removes temporary database at end of each test"""
		os.close(self.db_fd)
		os.unlink(self.db_path)

	def test_list_all(self):
		"""
		Get all members of Link Relations collection and verify that it's an empty data set
		"""
		resp = self.test_client.get('/rels/')
		data = json.loads(resp.data)

		(resp.status_code).should.equal(200)
		(len(data.keys())).should.equal(2)

	def test_select_all(self):
		"""
		Select all link relations and check them
		"""
		resp = self.test_client.get('/rels/')
		data = json.loads(resp.data)

		for rel_id in data.keys():
			resp = self.test_client.get('/rels/%s' % rel_id)
			schema = json.loads(resp.data)
			(Draft4Validator.check_schema(data)).should.be(None)

	def test_rel_not_found(self):
		"""Expect error object and message if rel not found"""
		resp = self.test_client.get('/rels/badrelname')
		data = json.loads(resp.data)

		(resp.status_code).should.equal(404)
		data['message'].should_not.be.different_of("Rel badrelname doesn't exist")