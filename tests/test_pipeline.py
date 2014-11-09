__author__ = 'DavidWCaraway'
from scraper.pipelines import DatabasePipeline
from scraper.items import BusinessItem
from scrapy.spider import Spider
import unittest
import tempfile
import os
import random
import sure
from app import create_application
from app.model import db, Organization, OrganizationSource, ContactPoint, Organization
from app.config import TestingConfig

class DatabasePipelineTest(unittest.TestCase):
    def setUp(self):
        """Construct temporary database and test client for testing routing and responses"""
        self.vitals = create_application(TestingConfig())

        #Push a context so that database knows what application to attach to
        with self.vitals.app_context():
            db.create_all()

    def tearDown(self):
        """Removes temporary database at end of each test"""
        with self.vitals.app_context():
            db.drop_all()
            db.session.remove()

    def test_basic(self):
        pipe = DatabasePipeline(self.vitals)

        sid = None
        
        with self.vitals.app_context(): 
            s = OrganizationSource(spider_name='testsrc')
            db.session.add(s)
            db.session.commit()
            sid = s.id

            len(Organization.query.all()).should.equal(0)

        item = BusinessItem()
        item['legalName']='myname'
        item['phone'] = 'myphone'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
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
            len(Organization.query.all()).should.equal(1)

    def test_missing_desc(self):
        pipe = DatabasePipeline(self.vitals)

        sid = None

        with self.vitals.app_context(): 
            s = OrganizationSource(spider_name='testsrc')
            db.session.add(s)
            db.session.commit()
            sid = s.id
            len(Organization.query.all()).should.equal(0)

        item = BusinessItem()
        item['legalName']='myname'
        item['phone'] = 'myphone'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['category'] = 'mycategory'
        item['address1'] = 'myaddress1'
        item['address2'] = 'myaddress2'
        item['city'] = 'mycity'
        item['state'] = 'mystate'
        item['zip'] = 'myzip'
        item['source_id'] = sid

        ret = pipe.process_item(item, Spider(name='foo'))

        ret.should.be(item) 

        with self.vitals.app_context():
            len(Organization.query.all()).should.equal(1)

    def test_existing(self):
        """An existing business should be updated"""

        biz_uid = None

        with self.vitals.app_context():
            b = Organization(legalName='oldname')

            db.session.add(b)
            db.session.commit()

            s = OrganizationSource(data_uid='123', spider_name='daytonlocal.com', organization_id=b.id)
            db.session.add(s)
            db.session.commit()

            biz_uid = b.id

        item = BusinessItem()
        item['legalName']='newname'
        item['source_data_id'] = '123'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='daytonlocal.com'))

        with self.vitals.app_context():
            b = Organization.query.get(biz_uid)
            b.legalName.should.equal('newname')

    def test_existing_by_phone(self):
            """If a business doesn't have a source_data_id
            then check to see if phone exists for that source id. if so,
            treat business as existing and modify rather than create 
            a new business.
            """
            
            biz_uid = None

            with self.vitals.app_context():
                s = OrganizationSource(spider_name='daytonchamber.org')
                db.session.add(s)
                db.session.commit()

                random_name = 'oldname{0}'.format(random.randint(1, 99))
                b = Organization(legalName=random_name)
                db.session.add(b)
                db.session.commit()

                cc = ContactPoint(telephone='12342342345', organization_id=b.id)
                db.session.add(cc)

                #Create a scraped BusinessItem with matching src and phone
                item = BusinessItem(legalName='newname', phone='12342342345', source_id=s.id)

                pipe = DatabasePipeline(self.vitals)
                pipe.process_item(item, Spider(name='daytonchamber.org'))

                #Business should have been modified. If not, then
                # a new business was mistakenly created.
                c = ContactPoint.query.filter_by(telephone='12342342345').first()
                c.organization.shouldnot.equal(None)
                c.organization.legalName.should.equal('newname')
                len(Organization.query.all()).should.equal(1)

