import unittest
import sure
import app as evented

class EventTest(unittest.TestCase):
	def setup(self):
		self.db_fd, evented.config['DATABASE'] = tempfile.mkstemp()
		evented.config['TESTING'] = True
		self.app = flaskr.app.test_client()
		flaskr.init_db()

	def teardown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])

	def test_addition(self):
		(2+2).should.equal(4)
