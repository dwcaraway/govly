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
            # s = OrganizationSource(spider_name='testsrc', data_url='http://www.foo.com')
            # db.session.add(s)
            # db.session.commit()
            # sid = s.id

            len(Organization.query.all()).should.equal(0)

        item = BusinessItem()
        item['legalName']='myname'
        item['phone'] = 'myphone'
        item['email'] = 'myemail'
        item['website'] = 'mywebsite'
        item['image_urls'] = 'mylogo'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['linkedin'] = 'mylinkedin'
        item['category'] = 'mycategory'
        item['description'] = 'mydescription'
        item['streetAddress'] = 'myaddress1'
        item['city'] = 'mycity'
        item['state'] = 'mystate'
        item['zip'] = 'myzip'
        item['source_url'] = 'http://www.somefoosomewhere.com'
        item['data_uid'] = 'source_data_id'

        ret = pipe.process_item(item, Spider(name='foo'))

        with self.vitals.app_context():
            o = Organization.query.first()
            o.shouldnot.equal(None)

            o.legalName.should.equal(item['legalName'])
            o.streetAddress.should.equal(item['streetAddress'])
            o.addressLocality.should.equal(item['city'])
            o.addressRegion.should.equal(item['state'])
            o.postalCode.should.equal(item['zip'])
            o.description.should.equal(item['description'])


    def test_missing_desc(self):
        pipe = DatabasePipeline(self.vitals)

        sid = None

        # with self.vitals.app_context():
        #     s = OrganizationSource(spider_name='testsrc', data_url='http://www.foo.com')
        #     db.session.add(s)
        #     db.session.commit()
        #     sid = s.id
        #     len(Organization.query.all()).should.equal(0)

        item = BusinessItem()
        item['legalName']='myname'
        item['phone'] = 'myphone'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['category'] = 'mycategory'
        item['streetAddress'] = 'myaddress1'
        item['city'] = 'mycity'
        item['state'] = 'mystate'
        item['zip'] = 'myzip'
        item['source_url'] = 'http://www.somefoosomewhere.com'

        ret = pipe.process_item(item, Spider(name='foo'))

        ret.should.be(item) 

        with self.vitals.app_context():
            len(Organization.query.all()).should.equal(1)

    def test_existing(self):
        """An existing business should be updated"""

        biz_uid = None

        with self.vitals.app_context():
            b = Organization(legalName='myname', postalCode='oldzip')

            db.session.add(b)
            db.session.commit()

            s = OrganizationSource(data_uid='123', spider_name='daytonlocal.com', organization_id=b.id, data_url='http://www.foo.com')
            db.session.add(s)
            db.session.commit()

            biz_uid = b.id

        item = BusinessItem()
        item['legalName']='myname'
        item['streetAddress'] = 'addr1'
        item['city'] = 'city'
        item['state'] = 'state'
        item['zip'] = 'newzip'
        item['data_uid'] = '123'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='daytonlocal.com'))

        with self.vitals.app_context():
            b = Organization.query.get(biz_uid)
            b.postalCode.should.equal('newzip')

    def test_existing_by_phone(self):
        """If a business doesn't have a data_uid
        then check to see if phone exists for that source id. if so,
        treat business as existing and modify rather than create
        a new business.
        """

        biz_uid = None

        with self.vitals.app_context():


            b = Organization(legalName='myname', addressLocality='originalcity')
            db.session.add(b)

            #OrganizationSource does not have a UID
            s = OrganizationSource(spider_name='daytonchamber.org', data_url='http://www.foo.com', organization=b)
            db.session.add(s)

            cc = ContactPoint(name='main', telephone='+1 234-234-2345', organization=b)
            db.session.add(cc)

            db.session.commit()

            #Create a scraped BusinessItem with matching src and phone, no unique id though
            item = BusinessItem(legalName='myname', phone='+1 234-234-2345', city='newcity')

            pipe = DatabasePipeline(self.vitals)
            pipe.process_item(item, Spider(name='daytonchamber.org'))

            #Business should have been modified. If not, then
            # a new business was mistakenly created.
            c = ContactPoint.query.filter_by(telephone='+1 234-234-2345').first()
            c.organization.shouldnot.equal(None)
            c.organization.addressLocality.should.equal('newcity')
            len(Organization.query.all()).should.equal(1)

    # def test_image_download(self):
    #     """Test local storage of images"""
    #     from scrapy.contrib.pipeline.images import ImagesPipeline
    #
    #     with self.vitals.app_context():
    #         pip = ImagesPipeline()
