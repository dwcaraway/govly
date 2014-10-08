__author__ = 'DavidWCaraway'
from scraper.pipelines import DatabasePipeline
from scraper.items import BusinessItem
from scrapy.spider import Spider
import unittest
import tempfile
import os
from app import create_application
from app.model import db, Business, Source

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

        item = BusinessItem()
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

        ret = pipe.process_item(item, Spider(name='foo'))

        ret.should.be(item) 

        with self.vitals.app_context():
            len(Business.query.all()).should.equal(1)

    def test_missing_desc(self):
        pipe = DatabasePipeline(self.vitals)

        with self.vitals.app_context(): 
            len(Business.query.all()).should.equal(0)

        item = BusinessItem()
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

        ret = pipe.process_item(item, Spider(name='foo'))

        ret.should.be(item) 

        with self.vitals.app_context():
            len(Business.query.all()).should.equal(1)

    def test_existing(self):
        """An existing business should be updated"""

        biz_uid = None

        with self.vitals.app_context():
            b = Business()
            s = Source(name='daytonlocal.com')
            
            db.session.add(s)
            db.session.commit()

            b.name = 'oldname'
            b.source_data_id='123'
            b.source_id = s.id

            db.session.add(b)
            db.session.commit()

            biz_uid = b.id

            item = BusinessItem()
            item['name']='newname'
            item['data_uid'] = '123'

            pipe = DatabasePipeline(self.vitals)
            pipe.process_item(item, Spider(name='daytonlocal.com'))

            b = Business.query.get(biz_uid)
            b.name.should.equal('newname')

    def test_existing_by_phone(self):
            """If a business doesn't have a data_uid
            then check to see if phone exists for that source id. if so,
            treat business as existing and modify rather than create 
            a new business.
            """
            
            biz_uid = None

            with self.vitals.app_context():
                s = Source(name='daytonchamber.org')
                db.session.add(s)
                db.session.commit()

                b = Business()
                b.name = 'oldname'
                b.phone = '12342342345'
                b.source_id = s.id
                db.session.add(b)
                db.session.commit()

                #Create a scraped BusinessItem with matching src and phone
                item = BusinessItem()
                item['name']='newname'
                item['phone'] = '12342342345'

                pipe = DatabasePipeline(self.vitals)
                pipe.process_item(item, Spider(name='daytonchamber.org'))

                #Business should have been modified. If not, then
                # a new business was mistakenly created.
                b = Business.query.filter_by(name='newname').first()
                b.phone.should.equal('12342342345')
                len(Business.query.all()).should.equal(1)

