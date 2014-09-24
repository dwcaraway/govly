import unittest, sure, logging, tempfile, os
import app as vitals

logger = logging.getLogger(__name__)

class EventTest(unittest.TestCase):
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

	def test_get_events(self):
		"""
		Get all members of Event collection and verify that it's not None
		"""
		rv = self.test_client.get('/api/events')
		(rv).should_not.be.equal(None)
