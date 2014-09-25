import unittest, sure, logging, tempfile, os 
import app as vitals
from dougrain import Document

logger = logging.getLogger(__name__)

class DBTest(unittest.TestCase):
	def setUp(self):
		"""Construct temporary database and test client for testing routing and responses"""
		self.db_fd, self.db_path = tempfile.mkstemp()
		vitals.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % self.db_path
		vitals.app.config['TESTING'] = True
		vitals.db.create_all()

	def tearDown(self):
		"""Removes temporary database at end of each test"""
		os.close(self.db_fd)
		os.unlink(self.db_path)