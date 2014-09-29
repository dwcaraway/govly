__author__ = 'DavidWCaraway'
from scraper.pipelines import DatabasePipeline
from scraper.items import DaytonlocalItem
import unittest
import tempfile
import os
from app import create_application
from app.model import db, Business

class PipelinesTest(unittest.TestCase):
    def setUp(self):
        """Construct temporary database and test client for testing routing and responses"""
        self.db_fd, self.db_path = tempfile.mkstemp()

        config = {
        'SQLALCHEMY_DATABASE_URI':'sqlite:///%s' % self.db_path,
        'TESTING': True
        }

        self.vitals = create_application(config)

        #Push a context so that database knows what application to attach to
        with self.vitals.app_context():
            db.create_all()

    def tearDown(self):
        """Removes temporary database at end of each test"""
        with self.vitals.app_context():
            db.drop_all()
            db.session.remove()

        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_basic(self):
        pipe = DatabasePipeline(self.vitals)

        with self.vitals.app_context(): 
            len(Business.query.all()).should.equal(0)

        item = DaytonlocalItem()
        item['name']='myname'
        item['phone'] = 'myphone'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['logo'] = 'mylogo'
        item['category'] = 'mycategory'
        item['description'] = 'mydescription'
        item['address1'] = 'myaddress1'
        item['address2'] = 'myaddress2'
        item['city'] = 'mycity'
        item['state'] = 'mystate'
        item['zip'] = 'myzip'

        ret = pipe.process_item(item, None)

        ret.should.be(item) 

        with self.vitals.app_context():
            len(Business.query.all()).should.equal(1)

    def test_missing_desc(self):
        pipe = DatabasePipeline(self.vitals)

        with self.vitals.app_context(): 
            len(Business.query.all()).should.equal(0)

        item = DaytonlocalItem()
        item['name']='myname'
        item['phone'] = 'myphone'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['logo'] = 'mylogo'
        item['category'] = 'mycategory'
        item['address1'] = 'myaddress1'
        item['address2'] = 'myaddress2'
        item['city'] = 'mycity'
        item['state'] = 'mystate'
        item['zip'] = 'myzip'

        ret = pipe.process_item(item, None)

        ret.should.be(item) 

        with self.vitals.app_context():
            len(Business.query.all()).should.equal(1)

    def test_existing(self):
        pipe = DatabasePipeline(self.vitals)

        b = Business()
        b.uid

        item = DaytonlocalItem()
        item['name']='myname'
        item['phone'] = 'myphone'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['logo'] = 'mylogo'
        item['category'] = 'mycategory'
        item['address1'] = 'myaddress1'
        item['address2'] = 'myaddress2'
        item['city'] = 'mycity'
        item['state'] = 'mystate'
        item['zip'] = 'myzip'

        ret = pipe.process_item(item, None)

        ret.should.be(item) 

        with self.vitals.app_context():
            len(Business.query.all()).should.equal(1)