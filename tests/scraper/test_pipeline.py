__author__ = 'DavidWCaraway'
import unittest

from scrapy.spider import Spider
from sqlalchemy.orm import scoped_session, sessionmaker

from scraper.pipelines import DatabasePipeline
from scraper.items import BusinessItem
from app import create_app
from app.framework.sql import db
from app.models.model import (Organization, OrganizationSource, ContactPoint, Link)
from .settings import TestingConfig


class DatabasePipelineTest(unittest.TestCase):
    def setUp(self):
        """Construct temporary database and test client for testing routing and responses"""
        self.vitals = create_app(TestingConfig())

        #Push a context so that database knows what application to attach to
        with self.vitals.app_context():
            db.create_all()
            self.DBSession = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db.engine))

    def tearDown(self):
        """Removes temporary database at end of each test"""
        with self.vitals.app_context():
            db.drop_all()
            db.session.remove()


    def test_basic(self):
        pipe = DatabasePipeline(self.vitals)

        sid = None
        
        item = BusinessItem()
        item['legalName']='myname'
        item['telephone'] = 'myphone'
        item['email'] = 'myemail'
        item['website'] = 'mywebsite'
        item['image_urls'] = 'mylogo'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['linkedin'] = 'mylinkedin'
        item['category'] = 'mycategory'
        item['description'] = 'mydescription'
        item['streetAddress'] = 'myaddress1'
        item['addressLocality'] = 'mycity'
        item['addressRegion'] = 'mystate'
        item['postalCode'] = 'myzip'
        item['data_url'] = 'http://www.somefoosomewhere.com'
        item['data_uid'] = 'source_data_id'

        ret = pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            o = session.query(Organization).one()

            o.legalName.should.equal(item['legalName'])
            o.streetAddress.should.equal(item['streetAddress'])
            o.addressLocality.should.equal(item['addressLocality'])
            o.addressRegion.should.equal(item['addressRegion'])
            o.postalCode.should.equal(item['postalCode'])
            o.description.should.equal(item['description'])

        finally:
            session.close()


    def test_missing_desc(self):
        item = BusinessItem()
        item['legalName']='myname'
        item['telephone'] = 'myphone'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['category'] = 'mycategory'
        item['streetAddress'] = 'myaddress1'
        item['addressLocality'] = 'mycity'
        item['addressRegion'] = 'mystate'
        item['postalCode'] = 'myzip'
        item['data_url'] = 'http://www.somefoosomewhere.com'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            o = session.query(Organization).one()
            o.description.should.equal(None)
        finally:
            session.close()


    def test_existing(self):
        """An existing business should be updated"""

        biz_uid = None

        session = self.DBSession()
        try:
            b = Organization(legalName='myname', postalCode='oldzip')
            s = OrganizationSource(data_uid='123', spider_name='daytonlocal.com', organization=b, data_url='http://www.foo.com')

            session.add(b)
            session.commit()

            biz_uid = b.id
        finally:
            session.close()

        item = BusinessItem()
        item['legalName']='myname'
        item['streetAddress'] = 'addr1'
        item['addressLocality'] = 'addressLocality'
        item['addressRegion'] = 'addressRegion'
        item['postalCode'] = 'newzip'
        item['data_uid'] = '123'
        item['data_url'] = 'http://www.foo.com'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='daytonlocal.com'))

        session = self.DBSession()
        try:
            b = session.query(Organization).get(biz_uid)
            b.postalCode.should.equal('newzip')
        finally:
            session.close()

    def test_existing_by_phone(self):
        """If a business doesn't have a data_uid
        then check to see if telephone exists for that source id. if so,
        treat business as existing and modify rather than create
        a new business.
        """

        biz_uid = None

        session = self.DBSession()
        try:
            b = Organization(legalName='myname', addressLocality='originalcity')
            session.add(b)
            #OrganizationSource does not have a UID
            s = OrganizationSource(spider_name='daytonchamber.org', data_url='http://www.foo.com', organization=b)
            cc = ContactPoint(name='main', telephone='+1 234-234-2345', organization=b)
            session.commit()
        finally:
            session.close()

        #Create a scraped BusinessItem with matching src and telephone, no unique id though
        item = BusinessItem(legalName='myname', telephone='+1 234-234-2345', addressLocality='newcity', data_url='http://www.foo.com')

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='daytonchamber.org'))

            #Business should have been modified. If not, then
            # a new business was mistakenly created.
        session = self.DBSession()
        try:
            c = session.query(ContactPoint).filter(ContactPoint.telephone == '+1 234-234-2345').one()
            c.organization.shouldnot.equal(None)
            c.organization.addressLocality.should.equal('newcity')
            session.query(Organization).one()
        finally:
            session.close()

    def test_organization_source_saved(self):
        """A business item's source information should be saved"""
        item = BusinessItem()
        item['legalName']='myname'
        item['data_url'] = 'http://www.foo.com/somebusiness.html'
        item['data_uid'] = 'a32sdf'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            o = session.query(Organization).one()
            len(o.sources).should.equal(1)
            o.sources[0].data_url.should.equal(item['data_url'])
            o.sources[0].data_uid.should.equal(item['data_uid'])
        finally:
            session.close()

    def test_organization_keywords_saved(self):
        """A business item's keyword should be saved"""
        item = BusinessItem()
        item['legalName']='myname'
        item['category'] = 'legal attorney'
        item['data_url'] = 'http://www.foo.com/somebusiness.html'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            o = session.query(Organization).one()
            len(o.keywords).should.equal(1)
            o.keywords[0].keyword.should.equal(item['category'])
        finally:
            session.close()

    def test_organization_links_saved(self):
        """A business item's links should be saved"""
        item = BusinessItem()
        item['legalName']='myname'
        item['website'] = 'mywebsite'
        item['facebook'] = 'myfacebook'
        item['twitter'] = 'mytwitter'
        item['linkedin'] = 'mylinkedin'
        item['data_url'] = 'http://www.foo.com/somebusiness.html'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            o = session.query(Organization).one()
            len(o.links).should.equal(4)

            fb = session.query(Link).filter(Link.rel=='facebook').one()
            fb.href.should.equal(item['facebook'])

            web = session.query(Link).filter(Link.rel=='website').one()
            web.href.should.equal(item['website'])

            ln = session.query(Link).filter(Link.rel=='linkedin').one()
            ln.href.should.equal(item['linkedin'])

            tw = session.query(Link).filter(Link.rel=='twitter').one()
            tw.href.should.equal(item['twitter'])
        finally:
            session.close()

    def test_organization_contact_saved(self):
        """A business item's contacts should be saved"""
        item = BusinessItem()
        item['legalName']='myname'
        item['email'] = 'my@me.com'
        item['telephone'] = '12342342345'
        item['data_url'] = 'http://www.foo.com/somebusiness.html'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            o = session.query(Organization).one()
            len(o.contacts).should.equal(1)

            o.contacts[0].email.should.equal(item['email'])
            o.contacts[0].telephone.should.equal(item['telephone'])
        finally:
            session.close()

    def test_organization_contact_update(self):
        """Verifies that an organization contact can be updated"""
        session = self.DBSession()
        c=None
        try:
            o = Organization(legalName='myname')
            session.add(o)
            OrganizationSource(data_uid='345', spider_name='foo', data_url='http://www.bar.com/firstbusiness.html', organization=o)
            c = ContactPoint(email='you@you.com', telephone='12342342345', organization=o)
            session.commit()
        finally:
            session.close()

        item = BusinessItem()
        item['legalName']='myname'
        item['data_uid']='1234'
        item['email'] = 'my@me.com'
        item['telephone'] = '12342342345'
        item['data_url'] = 'http://www.foo.com/somebusiness.html'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            o = session.query(Organization).one()
            len(o.contacts).should.equal(1)
            o.contacts[0].email.should.equal(item['email'])
        finally:
            session.close()

    def test_multiple_contacts_bug(self):
        """Verifies that multiple contacts can be stored (had a bug where all contacts overwrote each other"""
        session = self.DBSession()
        c=None
        try:
            o = Organization(legalName='org1')
            session.add(o)
            c = ContactPoint(telephone='telephone1', organization=o)
            session.commit()
        finally:
            session.close()

        item = BusinessItem()
        item['legalName']='org2'
        item['data_uid']='1234'
        item['telephone'] = 'telephone2'
        item['data_url'] = 'http://www.foo.com/somebusiness.html'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            contacts = session.query(ContactPoint).all()
            len(contacts).should.equal(2)
        finally:
            session.close()

    def test_organization_with_no_data_uid(self):
        """Verifies that organization extracted data with no data_uid will use data_url for lookup"""
        session = self.DBSession()
        c=None
        try:
            o = Organization(legalName='org1', streetAddress='addr1')
            session.add(o)
            os = OrganizationSource(data_uid='1234', data_url='http://foo.com/bar?id=1234', spider_name='foo', organization=o)
            session.commit()
        finally:
            session.close()

        item = BusinessItem()
        item['legalName']='org1'
        item['streetAddress']= 'addr1'
        item['data_url']='http://foo.com/bar?id=1234'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            orgs = session.query(Organization).all()
            len(orgs).should.equal(1)
        finally:
            session.close()

    def test_organization_no_uid_false_duplicate(self):
        """
        Verifies that scraped organization with no data_uid,
        same data_url, same spider name but different legal names save as separate organizations.

        This example comes from the one page displays of business information (e.g. local dayton chamber)
        """
        session = self.DBSession()
        c=None
        try:
            o = Organization(legalName='org1', streetAddress='addr1')
            session.add(o)
            os = OrganizationSource(data_url='http://foo.com/bar', spider_name='foo', organization=o)
            session.commit()
        finally:
            session.close()

        item = BusinessItem()
        item['legalName']='org2'
        item['streetAddress']= 'addr2'
        item['data_url']='http://foo.com/bar'

        pipe = DatabasePipeline(self.vitals)
        pipe.process_item(item, Spider(name='foo'))

        session = self.DBSession()
        try:
            orgs = session.query(Organization).all()
            len(orgs).should.equal(2)
        finally:
            session.close()

    # def test_image_download(self):
    #     """Test local storage of images"""
    #     from scrapy.contrib.pipeline.images import ImagesPipeline
    #
    #     with self.vitals.app_context():
    #         pip = ImagesPipeline()
